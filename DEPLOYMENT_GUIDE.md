# Production Deployment Guide - ActionEDx AI Backend

## 🚀 Deployment Overview

This guide covers deploying ActionEDx AI Backend to production with all Phase 1-3 features.

---

## 📋 Pre-Deployment Checklist

### 1. Infrastructure Requirements

**Minimum Specs**:
- **Backend**: 2 vCPU, 4GB RAM (recommended: 4 vCPU, 8GB RAM)
- **Database**: MongoDB 5.0+ (Atlas M10+ or equivalent)
- **Cache**: Redis 7.0+ (2GB+ memory)
- **Storage**: 50GB+ SSD

**Services Needed**:
- [x] MongoDB (managed or self-hosted)
- [x] Redis (managed or self-hosted)
- [x] SSL Certificate (Let's Encrypt or commercial)
- [x] Domain name (api.actionedx.com)
- [ ] CDN (optional, for frontend assets)
- [ ] Load Balancer (optional, for high availability)

### 2. API Keys & Credentials

**Required**:
- [ ] Emergent LLM Key (for AI services)
- [ ] MongoDB connection string
- [ ] Redis connection URL
- [ ] JWT secret (generate with: `openssl rand -base64 32`)

**Optional**:
- [ ] OpenAI API key (if using direct OpenAI)
- [ ] Anthropic API key (if using direct Claude)
- [ ] Sentry DSN (for error tracking)
- [ ] AWS credentials (for S3 storage)
- [ ] SendGrid API key (for emails)

### 3. Security Setup

- [ ] Configure firewall (allow ports 80, 443 only)
- [ ] Set up SSL/TLS certificates
- [ ] Configure CORS for production domains
- [ ] Set strong JWT secret
- [ ] Enable rate limiting
- [ ] Configure IP whitelisting (if needed)
- [ ] Set up backup encryption

---

## 🔧 Deployment Steps

### Step 1: Environment Configuration

```bash
# Copy production environment template
cp .env.production.example backend/.env.production

# Edit with your production values
nano backend/.env.production
```

**Critical Settings**:
```bash
ENV=production
DEBUG=false
MONGO_URL="mongodb+srv://user:pass@cluster.mongodb.net/actionedx"
REDIS_URL="redis://user:pass@redis-host:6379/0"
EMERGENT_LLM_KEY="sk-emergent-your-key"
JWT_SECRET="your-super-secret-jwt-key"
CORS_ORIGINS="https://actionedx.com,https://app.actionedx.com"
```

### Step 2: Install Dependencies

```bash
# Backend
cd /app/backend
pip install -r requirements.txt

# Frontend
cd /app/frontend
yarn install
```

### Step 3: Database Setup

```bash
# Connect to MongoDB
mongo \"$MONGO_URL\"

# Create indexes
use actionedx
db.users.createIndex({ email: 1 }, { unique: true })
db.users.createIndex({ id: 1 }, { unique: true })
db.enrollments.createIndex({ user_id: 1, track_id: 1 })
db.analytics_events.createIndex({ user_id: 1, created_at: -1 })
```

### Step 4: Build Frontend

```bash
cd /app/frontend
yarn build

# Output will be in /app/frontend/build
# Serve with nginx or your preferred web server
```

### Step 5: Start Backend

**Option A: Supervisor (Recommended)**
```bash
sudo supervisorctl stop backend
sudo supervisorctl start backend
sudo supervisorctl status backend
```

**Option B: PM2**
```bash
pm2 start backend/server.py --name actionedx-backend
pm2 save
pm2 startup
```

**Option C: Systemd**
```bash
sudo systemctl start actionedx-backend
sudo systemctl enable actionedx-backend
sudo systemctl status actionedx-backend
```

### Step 6: Configure Nginx

```nginx
# /etc/nginx/sites-available/actionedx

upstream backend {
    server localhost:8001;
}

server {
    listen 80;
    server_name api.actionedx.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.actionedx.com;

    ssl_certificate /etc/letsencrypt/live/api.actionedx.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.actionedx.com/privkey.pem;

    # Security headers
    add_header X-Frame-Options \"DENY\" always;
    add_header X-Content-Type-Options \"nosniff\" always;
    add_header X-XSS-Protection \"1; mode=block\" always;
    add_header Strict-Transport-Security \"max-age=31536000\" always;

    # API endpoints
    location /api/ {
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # WebSocket support
    location /ws/ {
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection \"upgrade\";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        
        # WebSocket timeouts
        proxy_connect_timeout 7d;
        proxy_send_timeout 7d;
        proxy_read_timeout 7d;
    }

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
    limit_req zone=api_limit burst=20 nodelay;
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/actionedx /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Step 7: SSL Certificate

```bash
# Using Let's Encrypt
sudo certbot --nginx -d api.actionedx.com

# Auto-renewal
sudo certbot renew --dry-run
```

---

## 🧪 Post-Deployment Testing

### 1. Run Health Checks

```bash
# Automated health check
./backend/health_check.sh https://api.actionedx.com

# Expected output: ✅ All health checks passed!
```

### 2. Test All Endpoints

```bash
# Run API test suite
./test_api.sh
```

### 3. Load Testing

```bash
# Simple load test
./backend/simple_load_test.sh https://api.actionedx.com

# Or using locust (if installed)
locust -f backend/load_test.py --host=https://api.actionedx.com
# Open http://localhost:8089
```

### 4. Monitor Logs

```bash
# Backend logs
tail -f /var/log/actionedx/backend.log

# Nginx access logs
tail -f /var/log/nginx/access.log

# Nginx error logs
tail -f /var/log/nginx/error.log
```

---

## 📊 Monitoring Setup

### 1. Prometheus

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'actionedx'
    static_configs:
      - targets: ['api.actionedx.com']
    metrics_path: '/api/metrics'
    scheme: https
```

Start Prometheus:
```bash
prometheus --config.file=prometheus.yml
# Access: http://localhost:9090
```

### 2. Grafana

```bash
# Start Grafana
docker run -d -p 3001:3000 --name=grafana grafana/grafana

# Import dashboards from /app/monitoring/grafana/dashboards/
# - ai_performance.json
# - cost_tracking.json
# - system_health.json
```

### 3. Uptime Monitoring

Set up cron job for health checks:
```bash
# Edit crontab
crontab -e

# Add health check every 5 minutes
*/5 * * * * /app/backend/health_check.sh https://api.actionedx.com

# Add daily backup at 2 AM
0 2 * * * /app/backend/backup.sh
```

### 4. Error Tracking (Optional)

```python
# Add to backend/server.py
import sentry_sdk

sentry_sdk.init(
    dsn=os.environ.get('SENTRY_DSN'),
    environment=\"production\",
    traces_sample_rate=0.1
)
```

---

## 💾 Backup & Recovery

### Automated Backups

```bash
# Set environment variables
export MONGO_URL=\"your-mongodb-url\"
export BACKUP_DIR=\"/var/backups/actionedx\"
export RETENTION_DAYS=30

# Run backup
./backend/backup.sh

# Output: /var/backups/actionedx/actionedx_backup_YYYYMMDD_HHMMSS.tar.gz
```

### Restore from Backup

```bash
# Extract backup
tar -xzf actionedx_backup_20241223_020000.tar.gz

# Restore MongoDB
mongorestore --uri=\"$MONGO_URL\" \
    --gzip \
    --dir=actionedx_backup_20241223_020000/mongodb

# Restore Redis
redis-cli --rdb actionedx_backup_20241223_020000/redis_dump.rdb

# Restore environment files
cp actionedx_backup_20241223_020000/backend.env /app/backend/.env
```

### S3 Backup (Optional)

```bash
# Configure S3
export AWS_S3_BACKUP_BUCKET=\"actionedx-backups\"

# Backups will automatically upload to S3
./backend/backup.sh
```

---

## 🔒 Security Hardening

### 1. Firewall Configuration

```bash
# UFW (Ubuntu)
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS
sudo ufw enable

# Deny all other incoming
sudo ufw default deny incoming
sudo ufw default allow outgoing
```

### 2. Fail2Ban (DDoS Protection)

```bash
# Install
sudo apt install fail2ban

# Configure
sudo nano /etc/fail2ban/jail.local
```

```ini
[nginx-limit-req]
enabled = true
filter = nginx-limit-req
action = iptables-multiport[name=ReqLimit, port=\"http,https\"]
logpath = /var/log/nginx/error.log
findtime = 600
bantime = 7200
maxretry = 10
```

### 3. API Key Rotation

```bash
# Generate new JWT secret
openssl rand -base64 32

# Update .env.production
# Restart backend
sudo supervisorctl restart backend
```

---

## 📈 Scaling

### Horizontal Scaling

```bash
# Run multiple backend instances
pm2 start backend/server.py -i 4  # 4 instances

# Or with Docker
docker-compose up -d --scale backend=3
```

### Load Balancer (Nginx)

```nginx
upstream backend_cluster {
    least_conn;
    server backend1:8001;
    server backend2:8001;
    server backend3:8001;
}

server {
    location /api/ {
        proxy_pass http://backend_cluster;
    }
}
```

### Database Scaling

- MongoDB: Use replica sets for read scaling
- Redis: Use Redis Cluster for distributed caching

---

## 🐛 Troubleshooting

### Backend Won't Start

```bash
# Check logs
tail -f /var/log/supervisor/backend.err.log

# Common issues:
# 1. Missing environment variables
# 2. MongoDB connection failed
# 3. Port 8001 already in use
```

### High Memory Usage

```bash
# Check memory
free -h

# Redis memory
redis-cli INFO memory

# Restart services
sudo supervisorctl restart backend
```

### Slow Response Times

```bash
# Check circuit breakers
curl https://api.actionedx.com/api/circuit-breakers

# Check cache hit rate
curl https://api.actionedx.com/api/cache/stats

# Monitor with Prometheus
# Query: rate(ai_request_latency_seconds[5m])
```

---

## 📞 Support & Maintenance

### Regular Maintenance Tasks

**Daily**:
- Monitor error logs
- Check health checks
- Review alert notifications

**Weekly**:
- Review Prometheus metrics
- Check disk space
- Update dependencies (if needed)

**Monthly**:
- Rotate API keys
- Review and archive old logs
- Performance optimization review
- Security audit

### Emergency Contacts

- **DevOps Team**: ops@actionedx.com
- **On-Call**: +1-xxx-xxx-xxxx
- **Status Page**: status.actionedx.com

---

## 📚 Additional Resources

- **API Documentation**: `/app/API_REFERENCE.md`
- **Phase 1 Summary**: `/app/PHASE1_IMPLEMENTATION_SUMMARY.md`
- **Phase 2 Summary**: `/app/PHASE2_IMPLEMENTATION_SUMMARY.md`
- **Docker Setup**: `/app/README_DOCKER.md`
- **Security Config**: `/app/backend/security_config.py`

---

## ✅ Deployment Verification

After deployment, verify:

- [ ] All endpoints return 200 OK
- [ ] SSL certificate is valid
- [ ] Health checks pass
- [ ] Circuit breakers are closed
- [ ] Cache is connected
- [ ] Database is accessible
- [ ] Backups are running
- [ ] Monitoring is active
- [ ] Logs are being collected
- [ ] Rate limiting is enforced

**Run**: `./backend/health_check.sh https://api.actionedx.com`

---

**Deployment complete! Your ActionEDx AI Backend is production-ready! 🚀**
