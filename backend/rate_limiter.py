# Rate Limiter for ActionEDx AI Backend
# Redis-backed rate limiting with per-user and per-endpoint quotas

import time
from typing import Optional, Dict, Any, Tuple
from datetime import datetime, timedelta
import hashlib
import logging
from enum import Enum

logger = logging.getLogger(__name__)

class RateLimitTier(str, Enum):
    """Rate limit tiers for different user types"""
    FREE = "free"
    BASIC = "basic"
    PRO = "pro"
    ENTERPRISE = "enterprise"

class RateLimitConfig:
    """Rate limit configuration by tier and endpoint"""
    
    # Requests per minute by tier
    TIER_LIMITS = {
        RateLimitTier.FREE: {
            "requests_per_minute": 10,
            "requests_per_hour": 100,
            "requests_per_day": 500,
            "ai_tokens_per_day": 50000
        },
        RateLimitTier.BASIC: {
            "requests_per_minute": 30,
            "requests_per_hour": 500,
            "requests_per_day": 5000,
            "ai_tokens_per_day": 500000
        },
        RateLimitTier.PRO: {
            "requests_per_minute": 100,
            "requests_per_hour": 2000,
            "requests_per_day": 20000,
            "ai_tokens_per_day": 2000000
        },
        RateLimitTier.ENTERPRISE: {
            "requests_per_minute": 1000,
            "requests_per_hour": 10000,
            "requests_per_day": 100000,
            "ai_tokens_per_day": 10000000
        }
    }
    
    # Endpoint-specific multipliers
    ENDPOINT_MULTIPLIERS = {
        "/api/assistant/chat": 1.0,
        "/api/audit/9-pillar": 2.0,  # More expensive
        "/api/tricore/plan": 2.0,
        "/api/paths/generate": 1.5,
        "/api/analytics/user": 0.5,  # Less expensive
        "/api/health": 0.1  # Very cheap
    }

class RateLimiter:
    """Token bucket rate limiter with Redis backend"""
    
    def __init__(self, cache_manager=None):
        self.cache_manager = cache_manager
        self.local_cache: Dict[str, Dict[str, Any]] = {}  # Fallback to memory
    
    def _get_rate_limit_key(self, user_id: str, window: str) -> str:
        """Generate rate limit key"""
        return f"rate_limit:{user_id}:{window}"
    
    def _get_token_usage_key(self, user_id: str) -> str:
        """Generate token usage key"""
        return f"token_usage:{user_id}:daily"
    
    async def check_rate_limit(self, user_id: str, endpoint: str,
                              tier: RateLimitTier = RateLimitTier.FREE) -> Tuple[bool, Dict[str, Any]]:
        """Check if request is within rate limits"""
        
        # Get tier limits
        limits = RateLimitConfig.TIER_LIMITS[tier]
        
        # Get endpoint multiplier
        multiplier = RateLimitConfig.ENDPOINT_MULTIPLIERS.get(endpoint, 1.0)
        
        # Check each time window
        windows = [
            ("minute", 60, limits["requests_per_minute"]),
            ("hour", 3600, limits["requests_per_hour"]),
            ("day", 86400, limits["requests_per_day"])
        ]
        
        for window_name, window_seconds, limit in windows:
            # Adjust limit by multiplier
            adjusted_limit = int(limit * multiplier)
            
            allowed, info = await self._check_window(
                user_id=user_id,
                window=window_name,
                window_seconds=window_seconds,
                limit=adjusted_limit
            )
            
            if not allowed:
                return False, {
                    "allowed": False,
                    "tier": tier.value,
                    "limit": adjusted_limit,
                    "remaining": 0,
                    "reset_at": info["reset_at"],
                    "retry_after": info["retry_after"],
                    "window": window_name
                }
        
        # All windows passed
        return True, {
            "allowed": True,
            "tier": tier.value,
            "limits": {
                "minute": limits["requests_per_minute"],
                "hour": limits["requests_per_hour"],
                "day": limits["requests_per_day"]
            }
        }
    
    async def _check_window(self, user_id: str, window: str,
                          window_seconds: int, limit: int) -> Tuple[bool, Dict[str, Any]]:
        """Check rate limit for a specific time window"""
        
        key = self._get_rate_limit_key(user_id, window)
        current_time = time.time()
        
        # Try Redis first
        if self.cache_manager and self.cache_manager.redis_client:
            try:
                # Get current count
                count_str = await self.cache_manager.redis_client.get(key)
                count = int(count_str) if count_str else 0
                
                if count >= limit:
                    # Rate limit exceeded
                    ttl = await self.cache_manager.redis_client.ttl(key)
                    return False, {
                        "reset_at": current_time + ttl,
                        "retry_after": ttl
                    }
                
                # Increment counter
                await self.cache_manager.redis_client.incr(key)
                
                # Set expiry on first increment
                if count == 0:
                    await self.cache_manager.redis_client.expire(key, window_seconds)
                
                return True, {"remaining": limit - count - 1}
                
            except Exception as e:
                logger.error(f"Redis rate limit error: {e}")
                # Fall through to local cache
        
        # Fallback to local cache
        if key not in self.local_cache:
            self.local_cache[key] = {
                "count": 0,
                "reset_at": current_time + window_seconds
            }
        
        cache_entry = self.local_cache[key]
        
        # Reset if window expired
        if current_time >= cache_entry["reset_at"]:
            cache_entry["count"] = 0
            cache_entry["reset_at"] = current_time + window_seconds
        
        if cache_entry["count"] >= limit:
            return False, {
                "reset_at": cache_entry["reset_at"],
                "retry_after": int(cache_entry["reset_at"] - current_time)
            }
        
        cache_entry["count"] += 1
        return True, {"remaining": limit - cache_entry["count"]}
    
    async def increment_token_usage(self, user_id: str, tokens: int,
                                   tier: RateLimitTier = RateLimitTier.FREE) -> Tuple[bool, int]:
        """Track and limit token usage"""
        
        key = self._get_token_usage_key(user_id)
        limit = RateLimitConfig.TIER_LIMITS[tier]["ai_tokens_per_day"]
        
        # Try Redis
        if self.cache_manager and self.cache_manager.redis_client:
            try:
                # Get current usage
                usage_str = await self.cache_manager.redis_client.get(key)
                current_usage = int(usage_str) if usage_str else 0
                
                if current_usage + tokens > limit:
                    return False, current_usage
                
                # Increment
                new_usage = await self.cache_manager.redis_client.incrby(key, tokens)
                
                # Set daily expiry
                if current_usage == 0:
                    await self.cache_manager.redis_client.expire(key, 86400)
                
                return True, new_usage
                
            except Exception as e:
                logger.error(f"Token tracking error: {e}")
        
        # Fallback: no tracking in local cache (would need persistence)
        return True, 0
    
    async def get_user_quota_info(self, user_id: str,
                                 tier: RateLimitTier = RateLimitTier.FREE) -> Dict[str, Any]:
        """Get user's current quota usage"""
        
        limits = RateLimitConfig.TIER_LIMITS[tier]
        
        # Get token usage
        token_key = self._get_token_usage_key(user_id)
        token_usage = 0
        
        if self.cache_manager and self.cache_manager.redis_client:
            try:
                usage_str = await self.cache_manager.redis_client.get(token_key)
                token_usage = int(usage_str) if usage_str else 0
            except:
                pass
        
        return {
            "user_id": user_id,
            "tier": tier.value,
            "limits": limits,
            "current_usage": {
                "tokens_today": token_usage,
                "tokens_remaining": max(0, limits["ai_tokens_per_day"] - token_usage)
            },
            "percentage_used": {
                "tokens": (token_usage / limits["ai_tokens_per_day"]) * 100 if limits["ai_tokens_per_day"] > 0 else 0
            }
        }
    
    async def reset_user_limits(self, user_id: str):
        """Reset all rate limits for a user (admin function)"""
        
        if not self.cache_manager or not self.cache_manager.redis_client:
            return False
        
        try:
            # Delete all rate limit keys for user
            pattern = f"rate_limit:{user_id}:*"
            async for key in self.cache_manager.redis_client.scan_iter(match=pattern):
                await self.cache_manager.redis_client.delete(key)
            
            # Delete token usage
            token_key = self._get_token_usage_key(user_id)
            await self.cache_manager.redis_client.delete(token_key)
            
            logger.info(f"Reset rate limits for user: {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error resetting limits: {e}")
            return False


# Singleton instance
rate_limiter = RateLimiter()
