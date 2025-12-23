# Circuit Breaker for ActionEDx AI Backend
# Protects against cascading failures in AI model calls

import time
import asyncio
from typing import Optional, Dict, Any, Callable, Awaitable
from datetime import datetime, timedelta
from enum import Enum
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

class CircuitState(str, Enum):
    """Circuit breaker states"""
    CLOSED = "closed"  # Normal operation
    OPEN = "open"  # Blocking requests
    HALF_OPEN = "half_open"  # Testing if service recovered

@dataclass
class CircuitBreakerConfig:
    """Circuit breaker configuration"""
    failure_threshold: int = 5  # Failures before opening
    success_threshold: int = 2  # Successes in half-open to close
    timeout_seconds: int = 60  # Time before trying half-open
    half_open_max_calls: int = 3  # Max concurrent calls in half-open

class CircuitBreaker:
    """Circuit breaker implementation for AI service calls"""
    
    def __init__(self, name: str, config: Optional[CircuitBreakerConfig] = None):
        self.name = name
        self.config = config or CircuitBreakerConfig()
        
        # State
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time: Optional[float] = None
        self.opened_at: Optional[float] = None
        self.half_open_calls = 0
        
        # Metrics
        self.total_calls = 0
        self.total_failures = 0
        self.total_successes = 0
        self.total_rejected = 0
        
        logger.info(f"Circuit breaker '{name}' initialized: {self.config}")
    
    async def call(self, func: Callable[..., Awaitable], *args, **kwargs) -> Any:
        """Execute function with circuit breaker protection"""
        
        self.total_calls += 1
        
        # Check if circuit is open
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                logger.info(f"Circuit '{self.name}' transitioning to HALF_OPEN")
                self._transition_to_half_open()
            else:
                self.total_rejected += 1
                raise CircuitBreakerOpenError(
                    f"Circuit breaker '{self.name}' is OPEN. "
                    f"Retry after {self._time_until_retry():.1f}s"
                )
        
        # Check half-open call limit
        if self.state == CircuitState.HALF_OPEN:
            if self.half_open_calls >= self.config.half_open_max_calls:
                self.total_rejected += 1
                raise CircuitBreakerOpenError(
                    f"Circuit breaker '{self.name}' is HALF_OPEN but at max concurrent calls"
                )
            self.half_open_calls += 1
        
        # Execute function
        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result
            
        except Exception as e:
            self._on_failure()
            raise
        
        finally:
            if self.state == CircuitState.HALF_OPEN:
                self.half_open_calls -= 1
    
    def _on_success(self):
        """Handle successful call"""
        self.total_successes += 1
        self.failure_count = 0
        
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            logger.info(
                f"Circuit '{self.name}' HALF_OPEN success "
                f"({self.success_count}/{self.config.success_threshold})"
            )
            
            if self.success_count >= self.config.success_threshold:
                self._transition_to_closed()
    
    def _on_failure(self):
        """Handle failed call"""
        self.total_failures += 1
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        logger.warning(
            f"Circuit '{self.name}' failure "
            f"({self.failure_count}/{self.config.failure_threshold})"
        )
        
        if self.state == CircuitState.HALF_OPEN:
            # Single failure in half-open reopens circuit
            logger.warning(f"Circuit '{self.name}' failed in HALF_OPEN, reopening")
            self._transition_to_open()
            
        elif self.failure_count >= self.config.failure_threshold:
            logger.error(
                f"Circuit '{self.name}' threshold reached, opening circuit"
            )
            self._transition_to_open()
    
    def _transition_to_open(self):
        """Transition to OPEN state"""
        self.state = CircuitState.OPEN
        self.opened_at = time.time()
        self.success_count = 0
        logger.error(f"Circuit '{self.name}' is now OPEN")
    
    def _transition_to_half_open(self):
        """Transition to HALF_OPEN state"""
        self.state = CircuitState.HALF_OPEN
        self.success_count = 0
        self.half_open_calls = 0
        logger.info(f"Circuit '{self.name}' is now HALF_OPEN")
    
    def _transition_to_closed(self):
        """Transition to CLOSED state"""
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.opened_at = None
        logger.info(f"Circuit '{self.name}' is now CLOSED")
    
    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to attempt reset"""
        if self.opened_at is None:
            return False
        
        elapsed = time.time() - self.opened_at
        return elapsed >= self.config.timeout_seconds
    
    def _time_until_retry(self) -> float:
        """Calculate seconds until retry is allowed"""
        if self.opened_at is None:
            return 0.0
        
        elapsed = time.time() - self.opened_at
        remaining = self.config.timeout_seconds - elapsed
        return max(0.0, remaining)
    
    def get_state(self) -> Dict[str, Any]:
        """Get current circuit breaker state"""
        return {
            "name": self.name,
            "state": self.state.value,
            "failure_count": self.failure_count,
            "success_count": self.success_count,
            "config": {
                "failure_threshold": self.config.failure_threshold,
                "success_threshold": self.config.success_threshold,
                "timeout_seconds": self.config.timeout_seconds
            },
            "metrics": {
                "total_calls": self.total_calls,
                "total_successes": self.total_successes,
                "total_failures": self.total_failures,
                "total_rejected": self.total_rejected,
                "success_rate": (
                    (self.total_successes / self.total_calls * 100)
                    if self.total_calls > 0 else 100.0
                )
            },
            "opened_at": (
                datetime.fromtimestamp(self.opened_at).isoformat()
                if self.opened_at else None
            ),
            "retry_after_seconds": self._time_until_retry() if self.state == CircuitState.OPEN else 0
        }
    
    def reset(self):
        """Manually reset circuit breaker (admin function)"""
        logger.info(f"Manually resetting circuit '{self.name}'")
        self._transition_to_closed()


class CircuitBreakerOpenError(Exception):
    """Raised when circuit breaker is open"""
    pass


class CircuitBreakerManager:
    """Manages multiple circuit breakers"""
    
    def __init__(self):
        self.breakers: Dict[str, CircuitBreaker] = {}
        self._create_default_breakers()
    
    def _create_default_breakers(self):
        """Create default circuit breakers for AI models"""
        
        # More lenient config for AI models (they can be slow)
        ai_config = CircuitBreakerConfig(
            failure_threshold=5,
            success_threshold=2,
            timeout_seconds=60
        )
        
        # Create breakers for each AI model
        models = ["gpt-4o", "gpt-4-turbo", "claude-3-sonnet", "gemini-pro"]
        for model in models:
            self.breakers[model] = CircuitBreaker(f"ai_model_{model}", ai_config)
        
        # Stricter config for critical services
        critical_config = CircuitBreakerConfig(
            failure_threshold=3,
            success_threshold=2,
            timeout_seconds=30
        )
        
        self.breakers["database"] = CircuitBreaker("database", critical_config)
        self.breakers["cache"] = CircuitBreaker("cache", critical_config)
        
        logger.info(f"Created {len(self.breakers)} circuit breakers")
    
    def get_breaker(self, name: str) -> Optional[CircuitBreaker]:
        """Get circuit breaker by name"""
        return self.breakers.get(name)
    
    def get_or_create_breaker(self, name: str,
                             config: Optional[CircuitBreakerConfig] = None) -> CircuitBreaker:
        """Get existing or create new circuit breaker"""
        if name not in self.breakers:
            self.breakers[name] = CircuitBreaker(name, config)
        return self.breakers[name]
    
    def get_all_states(self) -> Dict[str, Dict[str, Any]]:
        """Get state of all circuit breakers"""
        return {
            name: breaker.get_state()
            for name, breaker in self.breakers.items()
        }
    
    def reset_all(self):
        """Reset all circuit breakers (admin function)"""
        for breaker in self.breakers.values():
            breaker.reset()
        logger.info("All circuit breakers reset")


# Singleton instance
circuit_breaker_manager = CircuitBreakerManager()
