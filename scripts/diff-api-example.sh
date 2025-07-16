#!/bin/bash
# Example of using the diff generation API with curl

set -e

BASE_URL="http://localhost:8080/api/v1/diffs"

echo "🚀 Diff Generation API Example (using curl)"
echo "=========================================="

# 1. Start diff generation
echo -e "\n1. Starting diff generation..."
RESPONSE=$(curl -s -X POST "$BASE_URL/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "branch": "HEAD",
    "base_branch": "main",
    "max_commits": 5
  }')

TASK_ID=$(echo "$RESPONSE" | grep -o '"task_id":"[^"]*' | cut -d'"' -f4)
echo "   Task ID: $TASK_ID"

# 2. Check status
echo -e "\n2. Checking status..."
while true; do
  STATUS_RESPONSE=$(curl -s "$BASE_URL/status/$TASK_ID")
  STATUS=$(echo "$STATUS_RESPONSE" | grep -o '"status":"[^"]*' | cut -d'"' -f4)
  
  echo -n "   Status: $STATUS"
  
  if [ "$STATUS" = "completed" ]; then
    COMMIT_COUNT=$(echo "$STATUS_RESPONSE" | grep -o '"commit_count":[0-9]*' | cut -d: -f2)
    echo -e "\n   ✅ Completed! Generated $COMMIT_COUNT diff files"
    break
  elif [ "$STATUS" = "failed" ]; then
    MESSAGE=$(echo "$STATUS_RESPONSE" | grep -o '"message":"[^"]*' | cut -d'"' -f4)
    echo -e "\n   ❌ Failed: $MESSAGE"
    exit 1
  else
    echo -n " (waiting...)"
    sleep 1
    echo -ne "\r\033[K"  # Clear line
  fi
done

# 3. Download index
echo -e "\n3. Downloading index.html..."
OUTPUT_DIR="diff-output-$TASK_ID"
mkdir -p "$OUTPUT_DIR"

curl -s "$BASE_URL/$TASK_ID/index.html" > "$OUTPUT_DIR/index.html"
echo "   ✅ Saved to: $OUTPUT_DIR/index.html"

# 4. Show how to serve
echo -e "\n4. To view the diffs:"
echo "   cd $OUTPUT_DIR && python -m http.server 8000"
echo "   Then open: http://localhost:8000"

echo -e "\n5. To clean up when done:"
echo "   curl -X DELETE $BASE_URL/$TASK_ID"