# ActionEDx AI Backend - Docker Setup

## Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+

## Quick Start

### 1. Start All Services

```bash
# Start all services in background
docker-compose up -d

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f redis
docker-compose logs -f prometheus
```

### 2. Access Services

- **Backend API**: http://localhost:8001
- **Frontend**: http://localhost:3000
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3001
  - Username: `admin`
  - Password: `actionedx2024`
- **MongoDB**: localhost:27017
- **Redis**: localhost:6379

### 3. Health Checks

```bash
# Check backend health
curl http://localhost:8001/api/health

# Check cache stats
curl http://localhost:8001/api/cache/stats

# Check Prometheus metrics
curl http://localhost:8001/api/metrics
```

### 4. Stop Services

```bash
# Stop all services
docker-compose stop

# Stop and remove containers
docker-compose down

# Stop and remove containers + volumes (WARNING: deletes data)
docker-compose down -v
```

## Development Workflow

### Redis CLI

```bash
# Access Redis CLI
docker exec -it actionedx-redis redis-cli

# Example commands in Redis CLI:
> KEYS *
> GET ai_cache:strategy_audit:gpt-4o:abc123
> DBSIZE
> INFO
```

### MongoDB CLI

```bash
# Access MongoDB shell
docker exec -it actionedx-mongodb mongosh

# Example commands:
use actionedx
db.users.find()
db.enrollments.countDocuments()
```

### Cache Management

```bash
# Clear all AI response cache
curl -X POST http://localhost:8001/api/cache/invalidate?pattern=ai_cache:*

# Clear session cache
curl -X POST http://localhost:8001/api/cache/invalidate?pattern=session:*
```

## Monitoring

### Prometheus Queries

Access Prometheus at http://localhost:9090 and try these queries:

```promql
# AI request rate
rate(ai_requests_total[5m])

# Average AI latency
rate(ai_request_latency_seconds_sum[5m]) / rate(ai_request_latency_seconds_count[5m])

# Cache hit rate
(rate(cache_operations_total{status="hit"}[5m]) / rate(cache_operations_total{operation="get"}[5m])) * 100

# Active WebSocket connections
websocket_active_connections

# AI cost per hour
rate(ai_cost_usd_total[1h]) * 3600
```

### Grafana Dashboards

1. Open http://localhost:3001
2. Login with admin/actionedx2024
3. Navigate to Dashboards
4. Import dashboard JSON from `monitoring/grafana/dashboards/`

## Troubleshooting

### Redis Connection Issues

```bash
# Check Redis is running
docker-compose ps redis

# Check Redis logs
docker-compose logs redis

# Test Redis connection
docker exec -it actionedx-redis redis-cli ping
```

### MongoDB Connection Issues

```bash
# Check MongoDB is running
docker-compose ps mongodb

# Check MongoDB logs
docker-compose logs mongodb

# Test MongoDB connection
docker exec -it actionedx-mongodb mongosh --eval "db.adminCommand('ping')"
```

### Service Health

```bash
# Check all container health
docker-compose ps

# Restart a specific service
docker-compose restart redis

# View resource usage
docker stats
```

## Production Considerations

1. **Redis Persistence**: Configure RDB snapshots and AOF
2. **MongoDB Backups**: Set up automated backups
3. **Prometheus Retention**: Adjust retention time based on needs
4. **Grafana Auth**: Change default password
5. **Resource Limits**: Set memory/CPU limits in docker-compose.yml
6. **Network Security**: Use Docker secrets for sensitive data
7. **SSL/TLS**: Configure HTTPS for production

## Scaling

For horizontal scaling:

```bash
# Scale backend services (if containerized)
docker-compose up -d --scale backend=3
```

## Backup & Restore

### MongoDB Backup

```bash
# Backup
docker exec actionedx-mongodb mongodump --out /backup

# Restore
docker exec actionedx-mongodb mongorestore /backup
```

### Redis Backup

```bash
# Backup (RDB snapshot)
docker exec actionedx-redis redis-cli BGSAVE

# Copy backup file
docker cp actionedx-redis:/data/dump.rdb ./redis-backup.rdb
```
