# AI Orchestrator - Multi-Model Routing and Execution
# Implements intelligent routing between AI models based on task requirements

import os
from typing import Dict, List, Any, Optional, Tuple
from emergentintegrations.llm.openai import LlmChat, UserMessage
from models import AIModel, TaskType, ModelCapability, AIRequestMetrics
from prompt_engine import ActionuityPromptEngine
import json
import uuid
import time
from datetime import datetime
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

EMERGENT_KEY = os.environ.get('EMERGENT_LLM_KEY')

# ==================== MODEL REGISTRY ====================

MODEL_CAPABILITIES: Dict[AIModel, ModelCapability] = {
    AIModel.GPT_4O: ModelCapability(
        model=AIModel.GPT_4O,
        strategy_planning=True,
        code_generation=True,
        creative_writing=True,
        analysis_synthesis=True,
        framework_alignment=True,
        ethical_guidance=True,
        cost_per_1k_tokens=0.005,
        max_tokens=128000,
        latency_ms=800
    ),
    AIModel.GPT_4_TURBO: ModelCapability(
        model=AIModel.GPT_4_TURBO,
        strategy_planning=True,
        code_generation=True,
        creative_writing=True,
        analysis_synthesis=True,
        framework_alignment=True,
        ethical_guidance=True,
        cost_per_1k_tokens=0.01,
        max_tokens=128000,
        latency_ms=1000
    ),
    AIModel.CLAUDE_3_SONNET: ModelCapability(
        model=AIModel.CLAUDE_3_SONNET,
        strategy_planning=True,
        code_generation=True,
        creative_writing=True,
        analysis_synthesis=True,
        framework_alignment=True,
        ethical_guidance=True,
        cost_per_1k_tokens=0.003,
        max_tokens=200000,
        latency_ms=600
    ),
    AIModel.GEMINI_PRO: ModelCapability(
        model=AIModel.GEMINI_PRO,
        strategy_planning=True,
        code_generation=True,
        creative_writing=True,
        analysis_synthesis=True,
        framework_alignment=True,
        ethical_guidance=True,
        cost_per_1k_tokens=0.00025,
        max_tokens=32000,
        latency_ms=500
    )
}

# Task to model routing preferences
TASK_MODEL_ROUTING: Dict[TaskType, List[AIModel]] = {
    TaskType.STRATEGY_AUDIT: [AIModel.GPT_4O, AIModel.CLAUDE_3_SONNET, AIModel.GPT_4_TURBO],
    TaskType.CODE_REVIEW: [AIModel.GPT_4O, AIModel.CLAUDE_3_SONNET],
    TaskType.CREATIVE_IDEATION: [AIModel.CLAUDE_3_SONNET, AIModel.GPT_4O],
    TaskType.ETHICAL_ASSESSMENT: [AIModel.CLAUDE_3_SONNET, AIModel.GPT_4O],
    TaskType.FRAMEWORK_ALIGNMENT: [AIModel.GPT_4O, AIModel.CLAUDE_3_SONNET],
    TaskType.REAL_TIME_TUTORING: [AIModel.GPT_4O, AIModel.GEMINI_PRO],
    TaskType.COLLABORATION_FACILITATION: [AIModel.GPT_4O, AIModel.CLAUDE_3_SONNET],
    TaskType.DOCUMENT_SYNTHESIS: [AIModel.CLAUDE_3_SONNET, AIModel.GPT_4O]
}

# Model provider mapping for LiteLLM
MODEL_PROVIDER_MAP: Dict[AIModel, Tuple[str, str]] = {
    AIModel.GPT_4O: ("openai", "gpt-4o"),
    AIModel.GPT_4_TURBO: ("openai", "gpt-4-turbo-preview"),
    AIModel.CLAUDE_3_SONNET: ("anthropic", "claude-3-sonnet-20240229"),
    AIModel.CLAUDE_3_OPUS: ("anthropic", "claude-3-opus-20240229"),
    AIModel.GEMINI_PRO: ("google", "gemini-pro"),
    AIModel.GEMINI_FLASH: ("google", "gemini-2.0-flash")
}


class AIOrchestrator:
    """Intelligent routing between AI models based on task characteristics"""
    
    def __init__(self):
        self.metrics: List[AIRequestMetrics] = []
        self.cache: Dict[str, Any] = {}
        self.active_sessions: Dict[str, LlmChat] = {}
        self.cache_manager = None  # Will be set during startup
    
    def set_cache_manager(self, cache_manager):
        """Set cache manager instance"""
        self.cache_manager = cache_manager
        logger.info("✅ Cache manager connected to AI Orchestrator")
    
    def route_request(self, task_type: TaskType, context: Dict[str, Any] = None,
                     prefer_model: AIModel = None) -> AIModel:
        """Route to optimal model based on task characteristics"""
        
        # If preferred model specified and valid, use it
        if prefer_model and prefer_model in MODEL_CAPABILITIES:
            return prefer_model
        
        # Get routing preferences for task
        preferred_models = TASK_MODEL_ROUTING.get(task_type, [AIModel.GPT_4O])
        
        # Score each model based on context
        if context:
            scored_models = []
            for model in preferred_models:
                score = self._score_model_for_context(model, task_type, context)
                scored_models.append((model, score))
            scored_models.sort(key=lambda x: x[1], reverse=True)
            return scored_models[0][0]
        
        return preferred_models[0]
    
    def _score_model_for_context(self, model: AIModel, task_type: TaskType,
                                context: Dict[str, Any]) -> float:
        """Score a model's suitability for given context"""
        
        capability = MODEL_CAPABILITIES.get(model)
        if not capability:
            return 0.0
        
        score = 50.0  # Base score
        
        # Adjust for task-specific capabilities
        task_capability_map = {
            TaskType.STRATEGY_AUDIT: 'strategy_planning',
            TaskType.CODE_REVIEW: 'code_generation',
            TaskType.CREATIVE_IDEATION: 'creative_writing',
            TaskType.ETHICAL_ASSESSMENT: 'ethical_guidance',
            TaskType.FRAMEWORK_ALIGNMENT: 'framework_alignment'
        }
        
        if task_type in task_capability_map:
            cap_name = task_capability_map[task_type]
            if getattr(capability, cap_name, False):
                score += 20.0
        
        # Adjust for latency requirements
        if context.get('low_latency_required', False):
            score -= capability.latency_ms / 100
        
        # Adjust for cost sensitivity
        if context.get('cost_sensitive', False):
            score -= capability.cost_per_1k_tokens * 1000
        
        # Adjust for content length
        content_length = context.get('content_length', 0)
        if content_length > capability.max_tokens * 0.5:
            score -= 10.0  # Penalize if content is large
        
        return score
    
    def get_fallback_models(self, primary_model: AIModel, task_type: TaskType) -> List[AIModel]:
        """Get fallback models for a given primary model and task"""
        
        all_models = TASK_MODEL_ROUTING.get(task_type, [AIModel.GPT_4O])
        return [m for m in all_models if m != primary_model]
    
    async def process_with_fallback(self, prompt: str, task_type: TaskType,
                                   context: Dict[str, Any] = None,
                                   system_message: str = None,
                                   prefer_model: AIModel = None) -> Dict[str, Any]:
        """Process request with automatic fallback on failure"""
        
        start_time = time.time()
        context = context or {}
        
        # Route to primary model
        primary_model = self.route_request(task_type, context, prefer_model)
        models_to_try = [primary_model] + self.get_fallback_models(primary_model, task_type)
        
        last_error = None
        
        for model in models_to_try:
            try:
                result = await self._call_model(
                    model=model,
                    prompt=prompt,
                    system_message=system_message,
                    context=context
                )
                
                # Validate response quality
                if self._validate_response(result, task_type):
                    latency_ms = int((time.time() - start_time) * 1000)
                    
                    # Record metrics
                    self._record_metrics(
                        model=model,
                        task_type=task_type,
                        latency_ms=latency_ms,
                        success=True,
                        tokens_used=result.get('tokens_used', 0)
                    )
                    
                    return {
                        "success": True,
                        "model": model.value,
                        "response": result['response'],
                        "latency_ms": latency_ms,
                        "tokens_used": result.get('tokens_used', 0)
                    }
                else:
                    last_error = "Response quality validation failed"
                    continue
                    
            except Exception as e:
                last_error = str(e)
                self._record_metrics(
                    model=model,
                    task_type=task_type,
                    latency_ms=int((time.time() - start_time) * 1000),
                    success=False
                )
                continue
        
        # All models failed
        return {
            "success": False,
            "error": f"All AI models failed: {last_error}",
            "fallback_response": self._generate_fallback_response(task_type)
        }
    
    async def _call_model(self, model: AIModel, prompt: str,
                         system_message: str = None,
                         context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Call a specific AI model"""
        
        provider, model_name = MODEL_PROVIDER_MAP.get(model, ("openai", "gpt-4o"))
        
        # Create session
        session_id = str(uuid.uuid4())
        sys_msg = system_message or "You are a helpful AI assistant for the Actionuity edX learning platform."
        
        llm_chat = LlmChat(
            api_key=EMERGENT_KEY,
            session_id=session_id,
            system_message=sys_msg
        ).with_model(provider, model_name)
        
        # Send message
        user_msg = UserMessage(text=prompt)
        response = await llm_chat.send_message(user_msg)
        
        return {
            "response": response,
            "tokens_used": len(prompt.split()) + len(response.split())  # Approximate
        }
    
    def _validate_response(self, result: Dict[str, Any], task_type: TaskType) -> bool:
        """Validate AI response meets quality standards"""
        
        response = result.get('response', '')
        
        # Basic validation
        if not response or len(response) < 50:
            return False
        
        # Task-specific validation
        if task_type == TaskType.STRATEGY_AUDIT:
            # Should contain audit elements
            return any(word in response.lower() for word in ['pillar', 'score', 'recommendation'])
        
        if task_type == TaskType.FRAMEWORK_ALIGNMENT:
            # Should reference framework elements
            return any(word in response.lower() for word in ['clarity', 'speed', 'ingenuity', 'framework'])
        
        return True
    
    def _generate_fallback_response(self, task_type: TaskType) -> str:
        """Generate fallback response when AI fails"""
        
        fallbacks = {
            TaskType.STRATEGY_AUDIT: "Strategy audit temporarily unavailable. Please try again or contact support.",
            TaskType.REAL_TIME_TUTORING: "I'm having trouble processing your request. Let me try a simpler approach. What specific question can I help you with?",
            TaskType.COLLABORATION_FACILITATION: "Collaboration assistance is temporarily limited. Please continue your discussion and I'll rejoin shortly.",
        }
        
        return fallbacks.get(task_type, "Service temporarily unavailable. Please try again.")
    
    def _record_metrics(self, model: AIModel, task_type: TaskType,
                       latency_ms: int, success: bool, tokens_used: int = 0):
        """Record request metrics"""
        
        capability = MODEL_CAPABILITIES.get(model)
        cost = (tokens_used / 1000) * capability.cost_per_1k_tokens if capability else 0
        
        metric = AIRequestMetrics(
            model=model.value,
            task_type=task_type.value,
            latency_ms=latency_ms,
            tokens_used=tokens_used,
            cost_usd=cost,
            success=success
        )
        
        self.metrics.append(metric)
        
        # Keep only last 1000 metrics in memory
        if len(self.metrics) > 1000:
            self.metrics = self.metrics[-1000:]
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get summary of AI metrics"""
        
        if not self.metrics:
            return {"total_requests": 0}
        
        total = len(self.metrics)
        successes = sum(1 for m in self.metrics if m.success)
        total_latency = sum(m.latency_ms for m in self.metrics)
        total_tokens = sum(m.tokens_used for m in self.metrics)
        total_cost = sum(m.cost_usd for m in self.metrics)
        
        # Model breakdown
        model_counts = {}
        for m in self.metrics:
            model_counts[m.model] = model_counts.get(m.model, 0) + 1
        
        return {
            "total_requests": total,
            "success_rate": successes / total if total > 0 else 0,
            "average_latency_ms": total_latency / total if total > 0 else 0,
            "total_tokens_used": total_tokens,
            "total_cost_usd": total_cost,
            "model_distribution": model_counts
        }


# Singleton instance
orchestrator = AIOrchestrator()
