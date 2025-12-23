# Redis Cache Manager for AI Responses and Sessions
# Provides caching layer for AI orchestrator with TTL strategies

import redis.asyncio as redis
import json
import hashlib
from typing import Optional, Any, Dict
import os
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

class CacheManager:
    """Redis-based cache manager for AI responses and sessions"""
    
    def __init__(self):
        self.redis_url = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
        self.redis_client: Optional[redis.Redis] = None
        self.default_ttl = 3600  # 1 hour
        
        # TTL strategies by task type
        self.ttl_strategies = {
            "strategy_audit": 86400,  # 24 hours
            "real_time_tutoring": 1800,  # 30 minutes
            "collaboration_facilitation": 3600,  # 1 hour
            "framework_alignment": 7200,  # 2 hours
            "ethical_assessment": 43200,  # 12 hours
            "code_review": 3600,  # 1 hour
            "creative_ideation": 7200,  # 2 hours
            "document_synthesis": 14400  # 4 hours
        }
    
    async def connect(self):
        """Connect to Redis"""
        try:
            self.redis_client = await redis.from_url(
                self.redis_url,
                encoding="utf-8",
                decode_responses=True,
                max_connections=50
            )
            # Test connection
            await self.redis_client.ping()
            logger.info(f"✅ Redis connected: {self.redis_url}")
        except Exception as e:
            logger.error(f"❌ Redis connection failed: {e}")
            self.redis_client = None
    
    async def disconnect(self):
        """Disconnect from Redis"""
        if self.redis_client:
            await self.redis_client.close()
            logger.info("Redis disconnected")
    
    def _generate_cache_key(self, prompt: str, task_type: str, 
                           model: str, context: Dict[str, Any] = None) -> str:
        """Generate cache key from request parameters"""
        
        # Create a deterministic hash of request parameters
        cache_data = {
            "prompt": prompt[:500],  # First 500 chars
            "task_type": task_type,
            "model": model,
            "context": json.dumps(context or {}, sort_keys=True)
        }
        
        cache_string = json.dumps(cache_data, sort_keys=True)
        cache_hash = hashlib.sha256(cache_string.encode()).hexdigest()[:16]
        
        return f"ai_cache:{task_type}:{model}:{cache_hash}"
    
    async def get_cached_response(self, prompt: str, task_type: str,
                                 model: str, context: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """Get cached AI response if available"""
        
        if not self.redis_client:
            return None
        
        try:
            cache_key = self._generate_cache_key(prompt, task_type, model, context)
            cached = await self.redis_client.get(cache_key)
            
            if cached:
                logger.info(f"✅ Cache HIT: {cache_key}")
                return json.loads(cached)
            else:
                logger.debug(f"❌ Cache MISS: {cache_key}")
                return None
                
        except Exception as e:
            logger.error(f"Cache get error: {e}")
            return None
    
    async def cache_response(self, prompt: str, task_type: str, model: str,
                           response: Dict[str, Any], context: Dict[str, Any] = None) -> bool:
        """Cache AI response with appropriate TTL"""
        
        if not self.redis_client:
            return False
        
        try:
            cache_key = self._generate_cache_key(prompt, task_type, model, context)
            ttl = self.ttl_strategies.get(task_type, self.default_ttl)
            
            await self.redis_client.setex(
                cache_key,
                ttl,
                json.dumps(response)
            )
            
            logger.info(f"✅ Cached response: {cache_key} (TTL: {ttl}s)")
            return True
            
        except Exception as e:
            logger.error(f"Cache set error: {e}")
            return False
    
    async def invalidate_cache(self, pattern: str = "ai_cache:*") -> int:
        """Invalidate cache entries matching pattern"""
        
        if not self.redis_client:
            return 0
        
        try:
            keys = []
            async for key in self.redis_client.scan_iter(match=pattern):
                keys.append(key)
            
            if keys:
                deleted = await self.redis_client.delete(*keys)
                logger.info(f"Invalidated {deleted} cache entries")
                return deleted
            return 0
            
        except Exception as e:
            logger.error(f"Cache invalidation error: {e}")
            return 0
    
    # ==================== SESSION MANAGEMENT ====================
    
    async def store_session(self, session_id: str, session_data: Dict[str, Any],
                          ttl: int = 7200) -> bool:
        """Store WebSocket session data"""
        
        if not self.redis_client:
            return False
        
        try:
            key = f"session:{session_id}"
            await self.redis_client.setex(
                key,
                ttl,
                json.dumps(session_data)
            )
            return True
        except Exception as e:
            logger.error(f"Session store error: {e}")
            return False
    
    async def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get WebSocket session data"""
        
        if not self.redis_client:
            return None
        
        try:
            key = f"session:{session_id}"
            session_data = await self.redis_client.get(key)
            
            if session_data:
                return json.loads(session_data)
            return None
            
        except Exception as e:
            logger.error(f"Session get error: {e}")
            return None
    
    async def update_session(self, session_id: str, updates: Dict[str, Any]) -> bool:
        """Update WebSocket session data"""
        
        session = await self.get_session(session_id)
        if session:
            session.update(updates)
            return await self.store_session(session_id, session)
        return False
    
    async def delete_session(self, session_id: str) -> bool:
        """Delete WebSocket session"""
        
        if not self.redis_client:
            return False
        
        try:
            key = f"session:{session_id}"
            await self.redis_client.delete(key)
            return True
        except Exception as e:
            logger.error(f"Session delete error: {e}")
            return False
    
    # ==================== ANALYTICS & MONITORING ====================
    
    async def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        
        if not self.redis_client:
            return {"status": "disconnected"}
        
        try:
            info = await self.redis_client.info("stats")
            keyspace = await self.redis_client.info("keyspace")
            
            # Count cache keys
            cache_keys = 0
            session_keys = 0
            
            async for key in self.redis_client.scan_iter(match="ai_cache:*"):
                cache_keys += 1
            
            async for key in self.redis_client.scan_iter(match="session:*"):
                session_keys += 1
            
            return {
                "status": "connected",
                "total_connections": info.get("total_connections_received", 0),
                "total_commands": info.get("total_commands_processed", 0),
                "cache_keys": cache_keys,
                "session_keys": session_keys,
                "keyspace_hits": info.get("keyspace_hits", 0),
                "keyspace_misses": info.get("keyspace_misses", 0),
                "hit_rate": self._calculate_hit_rate(info)
            }
            
        except Exception as e:
            logger.error(f"Cache stats error: {e}")
            return {"status": "error", "error": str(e)}
    
    def _calculate_hit_rate(self, info: Dict) -> float:
        """Calculate cache hit rate"""
        hits = info.get("keyspace_hits", 0)
        misses = info.get("keyspace_misses", 0)
        total = hits + misses
        
        if total == 0:
            return 0.0
        
        return (hits / total) * 100


# Singleton instance
cache_manager = CacheManager()
