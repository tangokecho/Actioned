#!/usr/bin/env bash
# Automated smoke tests for ActionEDx API
# Usage: ./test_api.sh

set -u -o pipefail

BASE_URL=${BASE_URL:-"http://localhost:8001/api"}
USER_ID=${TEST_USER_ID:-"doc-user-$RANDOM"}
TMP_DIR=$(mktemp -d)

GREEN="\033[32m"
RED="\033[31m"
YELLOW="\033[33m"
RESET="\033[0m"

pass() { echo -e "${GREEN}✔${RESET} $1"; }
fail() { echo -e "${RED}✖${RESET} $1"; }
skip() { echo -e "${YELLOW}⚠${RESET} $1"; }

call() {
  local method=$1
  local path=$2
  local data=${3:-}
  local url="$BASE_URL$path"
  local out_http
  local out_body="$TMP_DIR/resp.json"

  if [[ -n "$data" ]]; then
    out_http=$(curl -s -o "$out_body" -w "%{http_code}" -X "$method" "$url" \
      -H 'Content-Type: application/json' -d "$data")
  else
    out_http=$(curl -s -o "$out_body" -w "%{http_code}" -X "$method" "$url")
  fi

  echo "$out_http" > "$TMP_DIR/status.txt"
}

check() {
  local label=$1
  local expected=${2:-200}
  local status=$(cat "$TMP_DIR/status.txt")
  if [[ "$status" == "$expected" ]]; then
    pass "$label (HTTP $status)"
  else
    fail "$label (HTTP $status, see $TMP_DIR/resp.json)"
  fi
}

# 0) Prepare a user
call POST "/users" "{\"email\":\"$USER_ID@example.com\",\"name\":\"Doc User\",\"role\":\"learner\"}"
check "Create user $USER_ID" 200

# 1) Health and deployment
call GET "/health"
check "Health check"

call GET "/deployment-status"
check "Deployment status"

# 2) AI assistant chat
call POST "/assistant/chat" "{\"user_id\":\"$USER_ID\",\"message\":\"Share today's strategy\",\"mode\":\"strategist\"}"
check "AI assistant chat"

# 3) Learning patterns catalog
call GET "/analytics/patterns"
check "Learning patterns"

# 4) User analytics (after logging one event)
call POST "/analytics/event?user_id=$USER_ID&event_type=login&duration_minutes=5" "{\"event_data\":{\"source\":\"docs-test\"}}"
check "Log analytics event"

call GET "/analytics/user/$USER_ID"
check "User analytics"

# 5) Knowledge graph + adaptive path
call GET "/paths/knowledge-graph"
check "Knowledge graph"

call POST "/paths/generate-adaptive?user_id=$USER_ID&goal_track=ai-action-officer" "{\"skill_level\":\"intermediate\",\"goals\":[\"strategic_thinking\"],\"completed_tracks\":0}"
check "Generate adaptive path"

# 6) Guardrails and monitoring
call GET "/rate-limit/quota/$USER_ID"
check "Rate limit quota"

call GET "/circuit-breakers"
check "Circuit breakers"

call GET "/streaming/active"
check "Streaming status"

call GET "/cache/stats"
check "Cache stats"

call GET "/websocket/stats"
check "WebSocket stats"

call GET "/metrics"
check "Prometheus metrics"

# Cleanup hint
skip "Responses saved in $TMP_DIR for inspection"
