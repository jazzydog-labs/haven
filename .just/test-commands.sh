#!/usr/bin/env bash
# Test all just commands and generate validation results

set -e

RESULTS_FILE="tests/justfile-validation.json"
mkdir -p tests

echo "🧪 Testing all just commands..."
echo ""

# Start JSON output
echo '{' > "$RESULTS_FILE"
echo '  "timestamp": "'$(date -u +"%Y-%m-%dT%H:%M:%SZ")'",' >> "$RESULTS_FILE"
echo '  "results": [' >> "$RESULTS_FILE"

FIRST_RESULT=true
PASS_COUNT=0
FAIL_COUNT=0

# Test function
test_command() {
    local cmd="$1"
    local expected="$2"
    local description="${3:-}"
    
    printf "  Testing %-30s " "$cmd..."
    
    # Run the test
    if timeout 10s just --dry-run $cmd &>/dev/null; then
        status="pass"
        echo "✅"
        ((PASS_COUNT++))
    else
        status="fail"
        echo "❌"
        ((FAIL_COUNT++))
    fi
    
    # Add comma if not first result
    if [ "$FIRST_RESULT" = false ]; then
        echo "," >> "$RESULTS_FILE"
    fi
    FIRST_RESULT=false
    
    # Write result
    printf '    {
      "command": "%s",
      "status": "%s",
      "expected": "%s",
      "description": "%s"
    }' "$cmd" "$status" "$expected" "$description" >> "$RESULTS_FILE"
}

echo "🏗️  Testing root commands..."
test_command "help" "pass" "Show help"
test_command "--list" "pass" "List all commands"
test_command "bootstrap" "pass" "Bootstrap environment"
test_command "run" "pass" "Run all services"
test_command "stop-all" "pass" "Stop all services"
test_command "check" "pass" "Run quality checks"
test_command "clean" "pass" "Clean project"

echo ""
echo "🐳 Testing Docker commands..."
test_command "run-docker" "pass" "Start Docker services"
test_command "stop-docker" "pass" "Stop Docker services"
test_command "logs-docker" "pass" "View Docker logs"
test_command "ps-docker" "pass" "List Docker containers"

echo ""
echo "🗄️  Testing database commands..."
test_command "db-up" "pass" "Start database"
test_command "db-migrate" "pass" "Run migrations"
test_command "db-console" "pass" "Database console"
test_command "db-reset" "pass" "Reset database"

echo ""
echo "🧪 Testing test commands..."
test_command "test" "pass" "Run all tests"
test_command "test-python" "pass" "Run Python tests"
test_command "test-web" "pass" "Run web tests"
test_command "test-fast" "pass" "Run fast tests"

echo ""
echo "📦 Testing package commands..."
test_command "run-api" "pass" "Run API server"
test_command "run-web" "pass" "Run web server"
test_command "lint-python" "pass" "Lint Python code"
test_command "lint-web" "pass" "Lint web code"

# Close JSON arrays and object
echo "" >> "$RESULTS_FILE"
echo '  ],' >> "$RESULTS_FILE"
echo '  "summary": {' >> "$RESULTS_FILE"
echo '    "total": '$((PASS_COUNT + FAIL_COUNT))',' >> "$RESULTS_FILE"
echo '    "passed": '$PASS_COUNT',' >> "$RESULTS_FILE"
echo '    "failed": '$FAIL_COUNT'' >> "$RESULTS_FILE"
echo '  }' >> "$RESULTS_FILE"
echo '}' >> "$RESULTS_FILE"

echo ""
echo "========================================"
echo "✅ Passed: $PASS_COUNT"
echo "❌ Failed: $FAIL_COUNT"
echo "========================================"
echo ""
echo "📊 Results saved to: $RESULTS_FILE"