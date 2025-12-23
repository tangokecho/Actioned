# ActionEDx AI Backend - Complete API Reference

**Base URL**: `https://actionedx-ai.preview.emergentagent.com`

---

## 🏥 Health & Status Endpoints

### 1. Health Check
**GET** `/api/health`

Get comprehensive system health status including circuit breakers, services, and database.

```bash
curl https://actionedx-ai.preview.emergentagent.com/api/health
```

**Response**:
```json
{
  "status": "healthy",
  "database": "connected",
  "cache": "disconnected",
  "circuit_breakers": {
    "all_closed": true,
    "open_count": 0,
    "details": {...}
  },
  "services": {
    "real_time_assistant": "running",
    "strategy_audit": "running",
    ...
  }
}
```

### 2. Deployment Status
**GET** `/api/deployment-status`

```bash
curl https://actionedx-ai.preview.emergentagent.com/api/deployment-status
```

---

## 🤖 AI Services

### 3. Real-Time AI Assistant (Chat)
**POST** `/api/assistant/chat`

Chat with AI assistant in different modes (strategist, ally, oracle).

```bash
curl -X POST https://actionedx-ai.preview.emergentagent.com/api/assistant/chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "demo-user",
    "message": "Help me conduct a 9-Pillar strategy audit",
    "mode": "strategist"
  }'
```

**Modes**: `strategist`, `ally`, `oracle`

### 4. WebSocket Real-Time Assistant
**WS** `/ws/assistant/{session_id}?user_id={user_id}`

```javascript
const ws = new WebSocket('wss://actionedx-ai.preview.emergentagent.com/ws/assistant/session-123?user_id=demo-user');

ws.onopen = () => {
  ws.send(JSON.stringify({
    user_id: 'demo-user',
    message: 'Generate a strategy audit',
    mode: 'strategist',
    task_type: 'strategy_audit'
  }));
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Type:', data.type);
  console.log('Content:', data.response || data.message);
};
```

### 5. 9-Pillar Strategy Audit
**POST** `/api/audit/9-pillar`

Comprehensive strategy audit using 9-Pillar Framework.

```bash
curl -X POST https://actionedx-ai.preview.emergentagent.com/api/audit/9-pillar \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "demo-user",
    "project_data": {
      "title": "AI-Powered EdTech Platform",
      "description": "Building an AI learning assistant",
      "stage": "ideation",
      "team_size": 3
    },
    "focus_pillars": ["clarity", "speed", "impact"]
  }'
```

### 6. Tri-Core Loop Planning
**POST** `/api/plan/tricore`

Generate Tri-Core Loop execution plan (GPT → CODEX → AGENT).

```bash
curl -X POST https://actionedx-ai.preview.emergentagent.com/api/plan/tricore \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "demo-user",
    "strategy_context": {
      "objective": "Launch MVP in 30 days",
      "constraints": ["limited budget", "solo founder"],
      "target_market": "SMB founders"
    }
  }'
```

### 7. House of Hearts Review
**POST** `/api/review/house-of-hearts`

Conduct peer review using Courage, Compassion, Accountability framework.

```bash
curl -X POST https://actionedx-ai.preview.emergentagent.com/api/review/house-of-hearts \
  -H "Content-Type: application/json" \
  -d '{
    "submission_id": "proj-123",
    "reviewer_id": "reviewer-456",
    "submission_data": {
      "title": "My Innovation Project",
      "description": "Built AI tool for market research",
      "artifacts": ["link-to-demo"]
    }
  }'
```

---

## 🧠 Advanced Learning Analytics (Phase 3)

### 8. User Analytics & Pattern Detection
**GET** `/api/analytics/user/{user_id}`

Get comprehensive learning analytics with ML-powered pattern detection.

```bash
curl https://actionedx-ai.preview.emergentagent.com/api/analytics/user/demo-user
```

**Response**:
```json
{
  "user_id": "demo-user",
  "detected_patterns": [
    {
      "pattern": "rapid_prototyper",
      "confidence": 0.85,
      "recommendations": [...],
      "intervention_priority": 2
    }
  ],
  "dropout_risk": 0.25,
  "completion_probability": 0.75,
  "personalized_recommendations": [...],
  "intervention_needed": false
}
```

### 9. Learning Patterns Catalog
**GET** `/api/analytics/patterns`

Get all 7 detectable learning patterns.

```bash
curl https://actionedx-ai.preview.emergentagent.com/api/analytics/patterns
```

**Patterns**:
- Rapid Prototyper
- Deep Thinker
- Social Learner
- Needs Support
- Consistent Achiever
- Explorer
- Perfectionist

### 10. Predict Learning Outcome
**POST** `/api/analytics/predict-outcome`

Predict completion probability and dropout risk.

```bash
curl -X POST "https://actionedx-ai.preview.emergentagent.com/api/analytics/predict-outcome?user_id=demo-user&track_id=innovation-foundations"
```

---

## 🗺️ Adaptive Learning Paths (Phase 3)

### 11. Generate Adaptive Learning Path
**POST** `/api/paths/generate-adaptive`

Generate personalized learning path using A* pathfinding on knowledge graph.

```bash
curl -X POST "https://actionedx-ai.preview.emergentagent.com/api/paths/generate-adaptive?user_id=demo-user&goal_track=innovation-foundations" \
  -H "Content-Type: application/json" \
  -d '{
    "skill_level": "intermediate",
    "completed_tracks": 0,
    "goals": ["strategic_thinking", "innovation"]
  }'
```

**Response**:
```json
{
  "path_id": "path_demo-user_...",
  "sequence": ["concept_clarity", "skill_9_pillar", "track_innovation_foundations"],
  "nodes": [...],
  "metrics": {
    "total_hours": 220,
    "total_nodes": 3,
    "alignment_score": 85.0,
    "avg_difficulty": 0.4
  },
  "rationale": "Well-suited to your profile. Progressive difficulty...",
  "alternative_paths": [...]
}
```

### 12. Knowledge Graph Info
**GET** `/api/paths/knowledge-graph`

Get knowledge graph statistics.

```bash
curl https://actionedx-ai.preview.emergentagent.com/api/paths/knowledge-graph
```

### 13. Check Prerequisites
**GET** `/api/paths/prerequisites/{node_id}`

Get prerequisites for a learning node.

```bash
curl https://actionedx-ai.preview.emergentagent.com/api/paths/prerequisites/track_ai_action_officer
```

### 14. Validate Prerequisites
**POST** `/api/paths/validate-prerequisites`

Check if user has met all prerequisites.

```bash
curl -X POST "https://actionedx-ai.preview.emergentagent.com/api/paths/validate-prerequisites?user_id=demo-user&target_node_id=track_innovation_foundations"
```

---

## 🛡️ Production Features (Phase 2)

### 15. Rate Limit Quota
**GET** `/api/rate-limit/quota/{user_id}`

Get user's rate limit quota and usage.

```bash
curl "https://actionedx-ai.preview.emergentagent.com/api/rate-limit/quota/demo-user?tier=free"
```

**Tiers**: `free`, `basic`, `pro`, `enterprise`

**Response**:
```json
{
  "user_id": "demo-user",
  "tier": "free",
  "limits": {
    "requests_per_minute": 10,
    "requests_per_hour": 100,
    "requests_per_day": 500,
    "ai_tokens_per_day": 50000
  },
  "current_usage": {
    "tokens_today": 1500,
    "tokens_remaining": 48500
  }
}
```

### 16. Reset Rate Limits (Admin)
**POST** `/api/rate-limit/reset/{user_id}`

```bash
curl -X POST https://actionedx-ai.preview.emergentagent.com/api/rate-limit/reset/demo-user
```

### 17. Circuit Breakers Status
**GET** `/api/circuit-breakers`

Get all circuit breaker states.

```bash
curl https://actionedx-ai.preview.emergentagent.com/api/circuit-breakers
```

**Response**:
```json
{
  "ai_model_gpt-4o": {
    "state": "closed",
    "failure_count": 0,
    "metrics": {
      "total_calls": 150,
      "success_rate": 98.0
    }
  },
  ...
}
```

### 18. Circuit Breaker Details
**GET** `/api/circuit-breakers/{name}`

```bash
curl https://actionedx-ai.preview.emergentagent.com/api/circuit-breakers/ai_model_gpt-4o
```

### 19. Reset Circuit Breaker (Admin)
**POST** `/api/circuit-breakers/{name}/reset`

```bash
curl -X POST https://actionedx-ai.preview.emergentagent.com/api/circuit-breakers/ai_model_gpt-4o/reset
```

### 20. Active Streams
**GET** `/api/streaming/active`

```bash
curl https://actionedx-ai.preview.emergentagent.com/api/streaming/active
```

### 21. Cancel Stream
**POST** `/api/streaming/{stream_id}/cancel`

```bash
curl -X POST https://actionedx-ai.preview.emergentagent.com/api/streaming/stream-123/cancel
```

---

## 📊 Monitoring & Observability (Phase 1)

### 22. Prometheus Metrics
**GET** `/api/metrics`

Get Prometheus-format metrics.

```bash
curl https://actionedx-ai.preview.emergentagent.com/api/metrics
```

### 23. Cache Statistics
**GET** `/api/cache/stats`

```bash
curl https://actionedx-ai.preview.emergentagent.com/api/cache/stats
```

### 24. Invalidate Cache
**POST** `/api/cache/invalidate`

```bash
curl -X POST "https://actionedx-ai.preview.emergentagent.com/api/cache/invalidate?pattern=ai_cache:*"
```

### 25. Cache Health
**GET** `/api/cache/health`

```bash
curl https://actionedx-ai.preview.emergentagent.com/api/cache/health
```

### 26. WebSocket Statistics
**GET** `/api/websocket/stats`

```bash
curl https://actionedx-ai.preview.emergentagent.com/api/websocket/stats
```

### 27. AI Orchestrator Stats
**GET** `/api/monitoring/orchestrator/stats`

```bash
curl https://actionedx-ai.preview.emergentagent.com/api/monitoring/orchestrator/stats
```

### 28. AI Monitoring Metrics
**GET** `/api/monitoring/ai/metrics`

```bash
curl https://actionedx-ai.preview.emergentagent.com/api/monitoring/ai/metrics
```

---

## 📚 Data Management

### 29. Get All Tracks
**GET** `/api/tracks`

```bash
curl https://actionedx-ai.preview.emergentagent.com/api/tracks
```

### 30. Create User
**POST** `/api/users`

```bash
curl -X POST https://actionedx-ai.preview.emergentagent.com/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "email": "demo@example.com",
    "execution_tracks": [],
    "skill_graph": {}
  }'
```

---

## 🧪 Testing Workflow Examples

### Complete User Journey Test

```bash
# 1. Check system health
curl https://actionedx-ai.preview.emergentagent.com/api/health

# 2. Get learning patterns
curl https://actionedx-ai.preview.emergentagent.com/api/analytics/patterns

# 3. Analyze user
curl https://actionedx-ai.preview.emergentagent.com/api/analytics/user/demo-user

# 4. Generate learning path
curl -X POST "https://actionedx-ai.preview.emergentagent.com/api/paths/generate-adaptive?user_id=demo-user&goal_track=innovation-foundations" \
  -H "Content-Type: application/json" \
  -d '{"skill_level":"intermediate"}'

# 5. Check rate limits
curl "https://actionedx-ai.preview.emergentagent.com/api/rate-limit/quota/demo-user?tier=free"

# 6. Chat with AI assistant
curl -X POST https://actionedx-ai.preview.emergentagent.com/api/assistant/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id":"demo-user","message":"Help me start my innovation journey","mode":"strategist"}'

# 7. Request strategy audit
curl -X POST https://actionedx-ai.preview.emergentagent.com/api/audit/9-pillar \
  -H "Content-Type: application/json" \
  -d '{"user_id":"demo-user","project_data":{"title":"My Project","stage":"ideation"}}'
```

---

## 📈 Monitoring Queries

### Check System Performance

```bash
# Cache performance
curl https://actionedx-ai.preview.emergentagent.com/api/cache/stats

# Circuit breaker health
curl https://actionedx-ai.preview.emergentagent.com/api/circuit-breakers

# Active WebSocket connections
curl https://actionedx-ai.preview.emergentagent.com/api/websocket/stats

# AI orchestrator metrics
curl https://actionedx-ai.preview.emergentagent.com/api/monitoring/orchestrator/stats

# Prometheus metrics (sample)
curl https://actionedx-ai.preview.emergentagent.com/api/metrics | grep "ai_requests_total"
```

---

## 🔑 Authentication

Currently, all endpoints are public for development. In production, add:

```bash
# Example with auth header
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://actionedx-ai.preview.emergentagent.com/api/analytics/user/demo-user
```

---

## 📊 Response Codes

- `200 OK` - Success
- `201 Created` - Resource created
- `400 Bad Request` - Invalid input
- `404 Not Found` - Resource not found
- `429 Too Many Requests` - Rate limit exceeded
- `500 Internal Server Error` - Server error
- `503 Service Unavailable` - Circuit breaker open

---

## 🎯 Quick Reference

**Most Important Endpoints**:
1. Health: `/api/health`
2. Analytics: `/api/analytics/user/{user_id}`
3. Learning Path: `/api/paths/generate-adaptive`
4. AI Chat: `/api/assistant/chat`
5. Strategy Audit: `/api/audit/9-pillar`

**Total Endpoints**: 30+  
**Base URL**: `https://actionedx-ai.preview.emergentagent.com`

---

For more details, see:
- `/app/PHASE1_IMPLEMENTATION_SUMMARY.md`
- `/app/PHASE2_IMPLEMENTATION_SUMMARY.md`
- `/app/backend/server.py` (source code)
