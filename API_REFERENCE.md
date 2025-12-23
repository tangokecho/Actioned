# ActionEDx API Reference

This reference consolidates the backend endpoints exposed by the FastAPI service in `backend/server.py`. Use it as the single place to discover capabilities, payload formats, and quick-start commands for local verification.

## Base URL and Environment
- **Base REST URL**: `http://localhost:8001/api`
- **WebSocket**: `ws://localhost:8001/ws/assistant/{session_id}`
- Ensure the backend is running with access to MongoDB and Redis (`MONGO_URL` and `DB_NAME` env vars). Docker Compose in `docker-compose.yml` provisions dependencies.

## Authentication and Client Guidelines
- There is no global API key. Provide a `user_id` in request bodies or query parameters where required to associate analytics and personalization.
- For WebSocket chats, pass `user_id` as a query parameter and set a unique `{session_id}` in the URL.
- Always send JSON with `Content-Type: application/json` for POST requests.

## Quick Start (cURL)
Set a base URL for convenience:
```bash
export BASE_URL=${BASE_URL:-"http://localhost:8001/api"}
```
Common calls:
- Health check: `curl "$BASE_URL/health"`
- Deployment status: `curl "$BASE_URL/deployment-status"`
- AI chat: `curl -X POST "$BASE_URL/assistant/chat" -H 'Content-Type: application/json' \
    -d '{"user_id":"demo","message":"Give me a day 1 plan","mode":"strategist"}'`
- Generate adaptive path: `curl -X POST "$BASE_URL/paths/generate-adaptive?user_id=demo&goal_track=ai-action-officer"`
- Rate limit quota: `curl "$BASE_URL/rate-limit/quota/demo"`

## Endpoint Catalog (30+)
The table below lists primary endpoints grouped by purpose.

| Category | Method | Path | Purpose |
| --- | --- | --- | --- |
| Core | GET | `/` | Root service banner |
| Core | GET | `/health` | Health of orchestrator, cache, and breakers |
| Core | GET | `/deployment-status` | Deployment metadata and live endpoints |
| Users | POST | `/users` | Create a user |
| Users | GET | `/users/{user_id}` | Fetch a user |
| Users | GET | `/users/{user_id}/skill-graph` | Skill graph summary |
| Tracks | GET | `/tracks` | List execution tracks |
| Tracks | POST | `/tracks/{track_id}/enroll` | Enroll a user in a track |
| Tracks | GET | `/tracks/{track_id}/enrollment/{user_id}` | Enrollment status |
| Assistant | POST | `/assistant/chat` | Multi-mode AI assistant |
| Assistant | GET | `/assistant/modes` | Assistant voice/style metadata |
| Strategy | POST | `/audit/9-pillar` | Run strategy audit |
| Strategy | POST | `/tricore/plan` | Generate Tri-Core execution plan |
| Reviews | POST | `/review/house-of-hearts` | House of Hearts review |
| Learning Paths | POST | `/paths/generate` | Generate a learning path |
| Learning Paths | GET | `/paths/{user_id}` | Paths for a user |
| Crews | POST | `/crews` | Create crew |
| Crews | POST | `/crews/{crew_id}/join` | Join crew |
| Collaboration | POST | `/crews/mediate` | AI-mediated collaboration |
| Collaboration | POST | `/collaboration/session/start` | Start collaboration session |
| Projects | POST | `/projects` | Create project |
| Projects | GET | `/projects/{user_id}` | Projects for a user |
| Projects | POST | `/projects/{project_id}/tricore` | Attach Tri-Core plan |
| Analytics | GET | `/analytics/user/{user_id}` | User analytics (advanced) |
| Analytics | GET | `/analytics/platform` | Platform analytics |
| Analytics | POST | `/analytics/event` | Log analytics event |
| Monitoring | GET | `/monitoring/ai/metrics` | AI metrics snapshot |
| Monitoring | GET | `/monitoring/ai/cost-optimization` | Cost opportunities |
| Monitoring | GET | `/monitoring/ai/daily-report` | Daily AI report |
| Monitoring | GET | `/monitoring/orchestrator/stats` | Orchestrator stats |
| Cache | GET | `/cache/stats` | Cache statistics |
| Cache | POST | `/cache/invalidate` | Invalidate cache by pattern |
| Cache | GET | `/cache/health` | Cache health summary |
| Metrics | GET | `/metrics` | Prometheus exposition |
| WebSockets | GET | `/websocket/stats` | Active WebSocket stats |
| Rate Limits | GET | `/rate-limit/quota/{user_id}` | Rate-limit quota |
| Rate Limits | POST | `/rate-limit/reset/{user_id}` | Reset quotas |
| Circuit Breakers | GET | `/circuit-breakers` | All circuit breaker states |
| Circuit Breakers | GET | `/circuit-breakers/{name}` | Breaker detail |
| Circuit Breakers | POST | `/circuit-breakers/{name}/reset` | Reset breaker |
| Circuit Breakers | POST | `/circuit-breakers/reset-all` | Reset all breakers |
| Streaming | GET | `/streaming/active` | Active streams |
| Streaming | POST | `/streaming/{stream_id}/cancel` | Cancel stream |
| Patterns | GET | `/analytics/patterns` | Learning pattern catalog |
| Predictions | POST | `/analytics/predict-outcome` | Predict learning outcome |
| Adaptive Paths | POST | `/paths/generate-adaptive` | Knowledge-graph path |
| Knowledge Graph | GET | `/paths/knowledge-graph` | Graph size and types |
| Knowledge Graph | GET | `/paths/prerequisites/{node_id}` | Prerequisite nodes |
| Knowledge Graph | POST | `/paths/validate-prerequisites` | Validate readiness |
| Credentials | POST | `/credentials/issue` | Issue completion credential |
| WebSocket | WS | `/ws/assistant/{session_id}` | Real-time assistant stream |

## Request and Response Highlights
Key payloads are defined in `backend/models.py` and `backend/server.py`.

### AI Assistant Chat
`POST /assistant/chat`
```json
{
  "user_id": "learner-123",
  "message": "Give me the day-1 playbook",
  "mode": "strategist",
  "task_type": "real_time_tutoring",
  "context": {"current_track": "ai-action-officer"}
}
```
Response mirrors `AssistantResponse` with `response`, `mode`, `session_id`, `model_used`, `suggestions`, `next_logical_step`, latency, and token usage.

### Generate Adaptive Path
`POST /paths/generate-adaptive?user_id={id}&goal_track=ai-action-officer`
```json
{
  "skill_level": "intermediate",
  "goals": ["strategic_thinking", "innovation"],
  "completed_tracks": 0
}
```
Returns a generated sequence of knowledge-graph nodes, difficulty metrics, rationale, and alternative paths.

### Learning Patterns
`GET /analytics/patterns`
Returns a list of detectable patterns (`rapid_prototyper`, `deep_thinker`, `social_learner`, `needs_support`, `consistent_achiever`) with descriptions, strengths, and growth areas.

### Knowledge Graph Insights
- `GET /paths/knowledge-graph` returns node/edge counts and node-type distribution.
- `GET /paths/prerequisites/{node_id}` enumerates prerequisites for a node.
- `POST /paths/validate-prerequisites?user_id=...&target_node_id=...` checks whether a user has satisfied requirements.

### Production Guardrails
- **Rate limits**: `GET /rate-limit/quota/{user_id}` reports quota and consumption; `POST /rate-limit/reset/{user_id}` resets it.
- **Circuit breakers**: inspect with `GET /circuit-breakers` or drill into a specific breaker; reset via the corresponding POST endpoints.
- **Cache**: observe stats with `/cache/stats` or clear patterns with `/cache/invalidate`.
- **Streaming**: `/streaming/active` and `/streaming/{id}/cancel` track long-running streams.

## Testing Workflows
An automated smoke test script is provided at `./test_api.sh`.
- It exercises 13 major endpoints (health, deployment status, learning patterns, user analytics, knowledge graph, adaptive path generation, AI chat, rate limits, circuit breakers, streaming, cache, WebSocket stats, Prometheus metrics).
- Results are color-coded for quick interpretation.
- Run with:
  ```bash
  chmod +x test_api.sh
  ./test_api.sh
  ```
- Customize with `BASE_URL` (default `http://localhost:8001/api`) and `TEST_USER_ID` to reuse existing users.

## Notes
- Many endpoints read/write MongoDB collections; ensure the database is reachable before invoking write-heavy workflows.
- WebSocket streaming uses `session_id` and `user_id` query parameters and exposes typing indicators plus metrics instrumentation.
- Prometheus metrics at `/metrics` include cache, WebSocket, AI request, and service health gauges.
