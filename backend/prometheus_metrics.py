# Prometheus Metrics for ActionEDx AI Backend
# Exposes metrics for monitoring and alerting

from prometheus_client import Counter, Histogram, Gauge, Info, generate_latest, CONTENT_TYPE_LATEST
import time
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

# ==================== METRICS DEFINITIONS ====================

# Request metrics
ai_requests_total = Counter(
    'ai_requests_total',
    'Total AI requests',
    ['model', 'task_type', 'status']
)

ai_request_latency = Histogram(
    'ai_request_latency_seconds',
    'AI request latency in seconds',
    ['model', 'task_type'],
    buckets=(0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0, 120.0)
)

ai_tokens_used = Counter(
    'ai_tokens_used_total',
    'Total tokens used',
    ['model', 'task_type']
)

ai_cost_usd = Counter(
    'ai_cost_usd_total',
    'Total cost in USD',
    ['model', 'task_type']
)

ai_response_quality = Gauge(
    'ai_response_quality_score',
    'AI response quality score (0-1)',
    ['model', 'task_type']
)

# WebSocket metrics
websocket_connections = Gauge(
    'websocket_active_connections',
    'Number of active WebSocket connections'
)

websocket_messages_total = Counter(
    'websocket_messages_total',
    'Total WebSocket messages',
    ['direction']  # 'inbound' or 'outbound'
)

websocket_errors_total = Counter(
    'websocket_errors_total',
    'Total WebSocket errors',
    ['error_type']
)

# Cache metrics
cache_operations_total = Counter(
    'cache_operations_total',
    'Total cache operations',
    ['operation', 'status']  # operation: 'get', 'set', 'delete'; status: 'hit', 'miss', 'success', 'error'
)

cache_size_bytes = Gauge(
    'cache_size_bytes',
    'Cache size in bytes'
)

cache_keys_total = Gauge(
    'cache_keys_total',
    'Total number of cached keys',
    ['key_type']  # 'ai_response', 'session'
)

# Database metrics
db_operations_total = Counter(
    'db_operations_total',
    'Total database operations',
    ['collection', 'operation', 'status']
)

db_operation_latency = Histogram(
    'db_operation_latency_seconds',
    'Database operation latency',
    ['collection', 'operation'],
    buckets=(0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0)
)

# Service health metrics
service_health = Gauge(
    'service_health',
    'Service health status (1=healthy, 0=unhealthy)',
    ['service']
)

service_info = Info(
    'actionedx_service',
    'ActionEDx service information'
)

# Set service info
service_info.info({
    'version': '2.0.0',
    'name': 'ActionEDx AI Backend',
    'environment': 'production'
})

# ==================== HELPER FUNCTIONS ====================

class MetricsRecorder:
    """Helper class to record metrics"""
    
    @staticmethod
    def record_ai_request(model: str, task_type: str, latency_seconds: float,
                         tokens_used: int, cost_usd: float, success: bool,
                         quality_score: float = None):
        """Record AI request metrics"""
        
        status = 'success' if success else 'failure'
        
        ai_requests_total.labels(
            model=model,
            task_type=task_type,
            status=status
        ).inc()
        
        ai_request_latency.labels(
            model=model,
            task_type=task_type
        ).observe(latency_seconds)
        
        ai_tokens_used.labels(
            model=model,
            task_type=task_type
        ).inc(tokens_used)
        
        ai_cost_usd.labels(
            model=model,
            task_type=task_type
        ).inc(cost_usd)
        
        if quality_score is not None:
            ai_response_quality.labels(
                model=model,
                task_type=task_type
            ).set(quality_score)
    
    @staticmethod
    def record_websocket_connection(delta: int):
        """Update WebSocket connection count"""
        if delta > 0:
            websocket_connections.inc(delta)
        elif delta < 0:
            websocket_connections.dec(abs(delta))
    
    @staticmethod
    def record_websocket_message(direction: str):
        """Record WebSocket message"""
        websocket_messages_total.labels(direction=direction).inc()
    
    @staticmethod
    def record_websocket_error(error_type: str):
        """Record WebSocket error"""
        websocket_errors_total.labels(error_type=error_type).inc()
    
    @staticmethod
    def record_cache_operation(operation: str, status: str):
        """Record cache operation"""
        cache_operations_total.labels(
            operation=operation,
            status=status
        ).inc()
    
    @staticmethod
    def update_cache_stats(ai_cache_keys: int, session_keys: int):
        """Update cache statistics"""
        cache_keys_total.labels(key_type='ai_response').set(ai_cache_keys)
        cache_keys_total.labels(key_type='session').set(session_keys)
    
    @staticmethod
    def record_db_operation(collection: str, operation: str,
                           latency_seconds: float, success: bool):
        """Record database operation"""
        
        status = 'success' if success else 'failure'
        
        db_operations_total.labels(
            collection=collection,
            operation=operation,
            status=status
        ).inc()
        
        db_operation_latency.labels(
            collection=collection,
            operation=operation
        ).observe(latency_seconds)
    
    @staticmethod
    def update_service_health(service: str, is_healthy: bool):
        """Update service health status"""
        service_health.labels(service=service).set(1 if is_healthy else 0)


def get_metrics_output():
    """Get Prometheus metrics output"""
    return generate_latest()


# Initialize service health
MetricsRecorder.update_service_health('backend', True)
MetricsRecorder.update_service_health('database', True)
MetricsRecorder.update_service_health('cache', True)
MetricsRecorder.update_service_health('ai_orchestrator', True)
