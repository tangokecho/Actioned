#!/bin/bash
# ActionEDx API Test Suite
# Quick validation of all major endpoints

BASE_URL="https://ai-learning-path-25.preview.emergentagent.com"

echo "🚀 ActionEDx API Test Suite"
echo "============================"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test counter
PASS=0
FAIL=0

test_endpoint() {
    local name="$1"
    local url="$2"
    local method="${3:-GET}"
    local data="$4"
    
    echo -n "Testing ${name}... "
    
    if [ "$method" = "POST" ]; then
        response=$(curl -s -w "\n%{http_code}" -X POST "$url" \
            -H "Content-Type: application/json" \
            -d "$data" 2>/dev/null)
    else
        response=$(curl -s -w "\n%{http_code}" "$url" 2>/dev/null)
    fi
    
    http_code=$(echo "$response" | tail -n 1)
    body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" = "200" ] || [ "$http_code" = "201" ]; then
        echo -e "${GREEN}✓ PASS${NC} (HTTP $http_code)"
        ((PASS++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC} (HTTP $http_code)"
        ((FAIL++))
        return 1
    fi
}

echo "📊 Core Endpoints"
echo "-----------------"
test_endpoint "Health Check" "$BASE_URL/api/health"
test_endpoint "Deployment Status" "$BASE_URL/api/deployment-status"
echo ""

echo "🧠 Analytics Endpoints (Phase 3)"
echo "--------------------------------"
test_endpoint "Learning Patterns" "$BASE_URL/api/analytics/patterns"
test_endpoint "User Analytics" "$BASE_URL/api/analytics/user/test-user"
test_endpoint "Knowledge Graph" "$BASE_URL/api/paths/knowledge-graph"
echo ""

echo "🗺️ Learning Path Endpoints (Phase 3)"
echo "------------------------------------"
test_endpoint "Generate Adaptive Path" \
    "$BASE_URL/api/paths/generate-adaptive?user_id=test&goal_track=innovation-foundations" \
    "POST" \
    '{"skill_level":"intermediate"}'
echo ""

echo "🤖 AI Services"
echo "--------------"
test_endpoint "AI Assistant Chat" \
    "$BASE_URL/api/assistant/chat" \
    "POST" \
    '{"user_id":"test","message":"Hello","mode":"strategist"}'
echo ""

echo "🛡️ Production Features (Phase 2)"
echo "--------------------------------"
test_endpoint "Rate Limit Quota" "$BASE_URL/api/rate-limit/quota/test-user?tier=free"
test_endpoint "Circuit Breakers" "$BASE_URL/api/circuit-breakers"
test_endpoint "Streaming Status" "$BASE_URL/api/streaming/active"
echo ""

echo "📊 Monitoring (Phase 1)"
echo "----------------------"
test_endpoint "Cache Stats" "$BASE_URL/api/cache/stats"
test_endpoint "WebSocket Stats" "$BASE_URL/api/websocket/stats"
test_endpoint "Prometheus Metrics" "$BASE_URL/api/metrics"
echo ""

echo "============================"
echo -e "Results: ${GREEN}${PASS} passed${NC}, ${RED}${FAIL} failed${NC}"
echo ""

if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}🎉 All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}⚠️  Some tests failed${NC}"
    exit 1
fi
