#!/bin/bash
# Simple Load Test Script (without locust)
# Tests API endpoints with concurrent requests

BASE_URL="${1:-https://actionedx-ai.preview.emergentagent.com}"
CONCURRENT_USERS=10
REQUESTS_PER_USER=20

echo "🔥 ActionEDx Load Test"
echo "======================"
echo "Base URL: $BASE_URL"
echo "Concurrent Users: $CONCURRENT_USERS"
echo "Requests per User: $REQUESTS_PER_USER"
echo ""

# Function to test endpoint
test_endpoint() {
    local endpoint=$1
    local method=${2:-GET}
    local data=$3
    local user_id="load-test-$RANDOM"
    
    if [ "$method" = "POST" ]; then
        curl -s -w "\n%{http_code},%{time_total}" -X POST "$BASE_URL$endpoint" \
            -H "Content-Type: application/json" \
            -d "$data" -o /dev/null
    else
        curl -s -w "\n%{http_code},%{time_total}" "$BASE_URL$endpoint" -o /dev/null
    fi
}

# Test health endpoint
echo "Testing /api/health..."
for i in $(seq 1 $REQUESTS_PER_USER); do
    test_endpoint "/api/health" &
done
wait
echo "✓ Health endpoint tested"

# Test analytics patterns
echo "Testing /api/analytics/patterns..."
for i in $(seq 1 10); do
    test_endpoint "/api/analytics/patterns" &
done
wait
echo "✓ Analytics patterns tested"

# Test path generation
echo "Testing /api/paths/generate-adaptive..."
for i in $(seq 1 5); do
    user_id="test-$RANDOM"
    test_endpoint "/api/paths/generate-adaptive?user_id=$user_id&goal_track=innovation-foundations" \
        "POST" \
        '{"skill_level":"intermediate"}' &
done
wait
echo "✓ Path generation tested"

# Test AI assistant
echo "Testing /api/assistant/chat..."
for i in $(seq 1 5); do
    user_id="test-$RANDOM"
    test_endpoint "/api/assistant/chat" \
        "POST" \
        '{"user_id":"'$user_id'","message":"Hello","mode":"strategist"}' &
done
wait
echo "✓ AI assistant tested"

echo ""
echo "✅ Load test complete!"
echo "Check response times and errors above"
