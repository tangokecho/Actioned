# AI Monitoring and Metrics Service
# Prometheus-compatible metrics and cost optimization

from typing import Dict, List, Any
from datetime import datetime, timedelta
from models import AIRequestMetrics
import json

class AIMonitoring:
    """Comprehensive monitoring for AI services"""
    
    def __init__(self):
        self.metrics: List[AIRequestMetrics] = []
        self.alerts: List[Dict[str, Any]] = []
        self.cost_budget_daily_usd = 100.0
    
    def record_request(self, metric: AIRequestMetrics):
        """Record an AI request metric"""
        self.metrics.append(metric)
        
        # Check alerts
        self._check_alerts(metric)
        
        # Limit memory usage
        if len(self.metrics) > 10000:
            self.metrics = self.metrics[-10000:]
    
    def _check_alerts(self, metric: AIRequestMetrics):
        """Check and trigger alerts"""
        
        # Latency alert
        if metric.latency_ms > 30000:  # 30 seconds
            self.alerts.append({
                "type": "high_latency",
                "severity": "warning",
                "model": metric.model,
                "latency_ms": metric.latency_ms,
                "timestamp": datetime.utcnow().isoformat()
            })
        
        # Error alert
        if not metric.success:
            self.alerts.append({
                "type": "ai_error",
                "severity": "error",
                "model": metric.model,
                "task_type": metric.task_type,
                "timestamp": datetime.utcnow().isoformat()
            })
        
        # Cost alert (daily budget check)
        daily_cost = self.get_daily_cost()
        if daily_cost > self.cost_budget_daily_usd * 0.8:
            self.alerts.append({
                "type": "cost_warning",
                "severity": "warning",
                "daily_cost": daily_cost,
                "budget": self.cost_budget_daily_usd,
                "timestamp": datetime.utcnow().isoformat()
            })
    
    def get_daily_cost(self) -> float:
        """Get cost for current day"""
        today = datetime.utcnow().date()
        daily_metrics = [m for m in self.metrics 
                        if m.timestamp.date() == today]
        return sum(m.cost_usd for m in daily_metrics)
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get comprehensive metrics summary"""
        
        if not self.metrics:
            return {
                "total_requests": 0,
                "success_rate": 100.0,
                "average_latency_ms": 0,
                "total_cost_usd": 0,
                "model_distribution": {},
                "task_distribution": {}
            }
        
        total = len(self.metrics)
        successes = sum(1 for m in self.metrics if m.success)
        
        # Model distribution
        model_counts = {}
        for m in self.metrics:
            model_counts[m.model] = model_counts.get(m.model, 0) + 1
        
        # Task distribution
        task_counts = {}
        for m in self.metrics:
            task_counts[m.task_type] = task_counts.get(m.task_type, 0) + 1
        
        # Latency percentiles
        latencies = sorted([m.latency_ms for m in self.metrics])
        p50_idx = int(len(latencies) * 0.5)
        p95_idx = int(len(latencies) * 0.95)
        p99_idx = int(len(latencies) * 0.99)
        
        return {
            "total_requests": total,
            "success_rate": (successes / total) * 100 if total > 0 else 100,
            "average_latency_ms": sum(m.latency_ms for m in self.metrics) / total if total > 0 else 0,
            "latency_p50_ms": latencies[p50_idx] if latencies else 0,
            "latency_p95_ms": latencies[p95_idx] if latencies else 0,
            "latency_p99_ms": latencies[p99_idx] if latencies else 0,
            "total_tokens_used": sum(m.tokens_used for m in self.metrics),
            "total_cost_usd": sum(m.cost_usd for m in self.metrics),
            "daily_cost_usd": self.get_daily_cost(),
            "model_distribution": model_counts,
            "task_distribution": task_counts,
            "recent_alerts": self.alerts[-10:]
        }
    
    def identify_cost_opportunities(self) -> List[Dict[str, Any]]:
        """Identify AI cost optimization opportunities"""
        
        opportunities = []
        
        if not self.metrics:
            return opportunities
        
        # Check for expensive models on simple tasks
        simple_tasks = ["real_time_tutoring", "collaboration_facilitation"]
        expensive_models = ["gpt-4-turbo-preview", "claude-3-opus-20240229"]
        
        expensive_simple = [
            m for m in self.metrics 
            if m.task_type in simple_tasks and m.model in expensive_models
        ]
        
        if len(expensive_simple) > 10:
            potential_savings = len(expensive_simple) * 0.005  # Estimated
            opportunities.append({
                "type": "model_downgrade",
                "description": f"{len(expensive_simple)} simple tasks used expensive models",
                "estimated_savings_usd": potential_savings,
                "recommendation": "Use gpt-4o or gemini-pro for simple tasks"
            })
        
        # Check for high token usage
        high_token_requests = [m for m in self.metrics if m.tokens_used > 10000]
        if len(high_token_requests) > 5:
            opportunities.append({
                "type": "prompt_optimization",
                "description": f"{len(high_token_requests)} requests used >10k tokens",
                "estimated_savings_usd": len(high_token_requests) * 0.01,
                "recommendation": "Optimize prompts and implement chunking"
            })
        
        return opportunities
    
    def generate_daily_report(self) -> Dict[str, Any]:
        """Generate daily AI usage report"""
        
        summary = self.get_metrics_summary()
        opportunities = self.identify_cost_opportunities()
        
        return {
            "date": datetime.utcnow().date().isoformat(),
            "generated_at": datetime.utcnow().isoformat(),
            "summary": summary,
            "cost_optimization_opportunities": opportunities,
            "alerts_count": len(self.alerts),
            "recommendations": [
                "Monitor latency trends",
                "Review model selection for cost optimization",
                "Implement caching for repeated queries"
            ]
        }


# Singleton instance
ai_monitoring = AIMonitoring()
