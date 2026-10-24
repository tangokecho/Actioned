# ActionEDx local infrastructure

This Compose file starts MongoDB, Redis, Prometheus and Grafana. It does **not** start the backend or frontend. This is a development setup, not a production deployment.

## Start

1. Copy `.env.example` to `.env` and set a unique `GRAFANA_ADMIN_PASSWORD`.
2. Run `docker compose config --quiet` to validate configuration.
3. Run `docker compose up -d`.
4. Inspect `docker compose ps` and `docker compose logs --tail=100`.

Host ports bind to loopback: MongoDB 27017, Redis 6379, Prometheus 9090, Grafana 3001. Grafana username is admin. Changing the environment password does not rotate an existing Grafana database password; use Grafana's password reset process for existing volumes.

## Application prerequisites

Run the backend separately on port 8001. It reads `backend/.env` and requires `MONGO_URL=mongodb://localhost:27017`, optional `DB_NAME=actionedx`, and the AI provider configuration. The source imports `emergentintegrations`, which is not declared in requirements.txt: resolve and pin the approved distribution before claiming a reproducible backend install.

The frontend lives in `frontend/` and declares Yarn 1.22.22. No lockfile is committed on main. Resolve dependencies and commit a reviewed lockfile before treating installs as reproducible.

Prometheus reaches a host backend through host.docker.internal. Linux host-gateway mapping is included; the backend must listen on an interface reachable from Docker, with firewall restrictions appropriate to the host. Prometheus will report the backend down until it can reach it. Redis requires an HTTP metrics exporter; it cannot be scraped directly on its database port.

## Checks and shutdown

- `python -m compileall -q backend tests`: syntax check only.
- `curl http://localhost:8001/api/health`: application response, **not proof of database or provider readiness**; current source contains hardcoded status values.
- `docker compose stop`: stop services, preserve containers and volumes.
- `docker compose down`: remove containers/network, preserve named volumes.

Never add `-v` unless intentionally deleting local database and dashboard data. Production requires authentication/authorization review, verified readiness probes, pinned images, backups with restore tests, and a separate deployment configuration.
