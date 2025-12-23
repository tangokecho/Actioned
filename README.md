# ActionEDx Platform

This repository contains the ActionEDx backend, frontend, and monitoring stack. Use the new API reference and smoke test harness to explore and verify the FastAPI service quickly.

## Documentation
- **API_REFERENCE.md** — full endpoint catalog (30+ routes), payload examples, and production guardrails.
- **PHASE1_IMPLEMENTATION_SUMMARY.md** / **PHASE2_IMPLEMENTATION_SUMMARY.md** — implementation notes by release phase.
- **README_DOCKER.md** — Docker Compose setup for MongoDB, Redis, Prometheus, and Grafana.

## Quick Start
1. Start the backend (ensure MongoDB/Redis are available):
   ```bash
   uvicorn backend.server:app --reload --port 8001
   ```
2. Run the curated smoke tests:
   ```bash
   chmod +x test_api.sh
   ./test_api.sh
   ```
3. Browse the API catalog and curl snippets in `API_REFERENCE.md` for deeper exploration.
