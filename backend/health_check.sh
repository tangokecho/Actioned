#!/bin/bash
# Health Check Script for Production Monitoring
# Run this via cron or monitoring service

BASE_URL="${1:-https://actionedx-ai.preview.emergentagent.com}"
ALERT_EMAIL="ops@actionedx.com"
LOG_FILE="/var/log/actionedx/health-check.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

timestamp() {
    date +"%Y-%m-%d %H:%M:%S"
}

log() {
    echo "[$(timestamp)] $1" | tee -a "$LOG_FILE"
}

alert() {
    local subject="$1"
    local message="$2"
    
    log "🚨 ALERT: $subject"
    log "$message"
    
    # Send email alert (requires mail command)
    if command -v mail &> /dev/null; then
        echo "$message" | mail -s "[ActionEDx] $subject" "$ALERT_EMAIL"
    fi
    
    # Send Slack notification (if webhook configured)
    if [ -n "$SLACK_WEBHOOK_URL" ]; then
        curl -X POST "$SLACK_WEBHOOK_URL" \
            -H 'Content-Type: application/json' \
            -d '{"text":"🚨 ActionEDx Alert: '"$subject"'"}'
    fi
}

# Check endpoint health
check_endpoint() {
    local endpoint=$1
    local name=$2
    local max_response_time=${3:-5}
    
    response=$(curl -s -w "\n%{http_code}\n%{time_total}" "$BASE_URL$endpoint" 2>/dev/null)
    http_code=$(echo "$response" | tail -n 2 | head -n 1)
    response_time=$(echo "$response" | tail -n 1)
    
    if [ "$http_code" != "200" ]; then
        echo -e "${RED}✗ $name FAILED${NC} (HTTP $http_code)"
        alert "$name Health Check Failed" "Endpoint: $endpoint\nHTTP Code: $http_code\nTime: $(timestamp)"
        return 1
    fi
    
    # Check response time
    if (( $(echo "$response_time > $max_response_time" | bc -l) )); then
        echo -e "${YELLOW}⚠ $name SLOW${NC} (${response_time}s)"
        log "WARNING: $name slow response: ${response_time}s"
    else
        echo -e "${GREEN}✓ $name OK${NC} (${response_time}s)"
    fi
    
    return 0
}

# Check circuit breakers
check_circuit_breakers() {
    response=$(curl -s "$BASE_URL/api/circuit-breakers")
    
    # Count open breakers
    open_count=$(echo "$response" | grep -o '"state":"open"' | wc -l)
    
    if [ "$open_count" -gt 0 ]; then
        echo -e "${RED}✗ Circuit Breakers: $open_count OPEN${NC}"
        alert "Circuit Breakers Open" "$open_count circuit breakers are in OPEN state"
        return 1
    else
        echo -e "${GREEN}✓ Circuit Breakers: All CLOSED${NC}"
        return 0
    fi
}

# Check database connectivity
check_database() {
    response=$(curl -s "$BASE_URL/api/health")
    db_status=$(echo "$response" | grep -o '"database":"[^"]*"' | cut -d'"' -f4)
    
    if [ "$db_status" != "connected" ]; then
        echo -e "${RED}✗ Database: $db_status${NC}"
        alert "Database Connection Failed" "Database status: $db_status"
        return 1
    else
        echo -e "${GREEN}✓ Database: connected${NC}"
        return 0
    fi
}

# Check cache
check_cache() {
    response=$(curl -s "$BASE_URL/api/cache/stats")
    cache_status=$(echo "$response" | grep -o '"status":"[^"]*"' | cut -d'"' -f4)
    
    if [ "$cache_status" = "connected" ]; then
        echo -e "${GREEN}✓ Cache: connected${NC}"
    else
        echo -e "${YELLOW}⚠ Cache: $cache_status${NC}"
        log "WARNING: Cache not connected"
    fi
}

# Main health check
log "==== Starting Health Check ===="

FAILURES=0

echo "📊 Checking Core Endpoints..."
check_endpoint "/api/health" "Health" 2 || ((FAILURES++))
check_endpoint "/api/tracks" "Tracks" 3 || ((FAILURES++))

echo ""
echo "🧠 Checking AI Services..."
check_endpoint "/api/analytics/patterns" "Analytics" 3 || ((FAILURES++))
check_endpoint "/api/paths/knowledge-graph" "Knowledge Graph" 3 || ((FAILURES++))

echo ""
echo "🛡️ Checking Production Features..."
check_circuit_breakers || ((FAILURES++))
check_database || ((FAILURES++))
check_cache

echo ""
echo "==================================="

if [ $FAILURES -eq 0 ]; then
    echo -e "${GREEN}✅ All health checks passed!${NC}"
    log "Health check: ALL PASSED"
    exit 0
else
    echo -e "${RED}❌ $FAILURES health checks failed!${NC}"
    log "Health check: $FAILURES FAILED"
    exit 1
fi
