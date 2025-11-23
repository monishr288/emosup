#!/bin/bash
# Red Team Testing Script for EmoSupport Advanced Features

echo "🔴 RED TEAM TESTING: Full Integration Test"
echo "=========================================="
echo ""

SESSION_ID="redteam-$(date +%s)"
API_URL="http://localhost:5000/api/therapy"

# Test 1: First message (should use basic therapy, depth=1)
echo "Test 1: First message (conversation_depth=1)"
echo "Expected: Basic CBT/DBT, NO advanced frameworks"
echo "---"
RESP1=$(curl -s -X POST "$API_URL" \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"I feel really anxious about work\", \"session_id\": \"$SESSION_ID\"}")

echo "$RESP1" | python3 -c "
import json, sys
d = json.load(sys.stdin)
print(f'✓ Emotion detected: {d.get(\"emotion\")}')
print(f'✓ Therapy mode: {d.get(\"therapy_mode\")}')
print(f'✓ Session phase: {d.get(\"session_phase\")}')
print(f'✓ Response length: {len(d.get(\"response\", \"\"))} chars')
print(f'✓ Techniques suggested: {len(d.get(\"suggested_techniques\", []))}')
print(f'  Preview: {d.get(\"response\", \"\")[:100]}...')
"
echo ""
sleep 1

# Test 2: Second message (depth=2, should try advanced frameworks)
echo "Test 2: Second message (conversation_depth=2)"
echo "Expected: Basic therapy (depth check happens at >=2 but might not trigger yet)"
echo "---"
RESP2=$(curl -s -X POST "$API_URL" \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"I always mess everything up\", \"session_id\": \"$SESSION_ID\"}")

echo "$RESP2" | python3 -c "
import json, sys
d = json.load(sys.stdin)
print(f'✓ Emotion: {d.get(\"emotion\")}')
print(f'✓ Therapy mode: {d.get(\"therapy_mode\")}')
print(f'✓ Distortions detected: {d.get(\"detected_distortions\", [])}')
print(f'  Response: {d.get(\"response\", \"\")[:100]}...')
"
echo ""
sleep 1

# Test 3: Third message (depth=3, advanced frameworks should activate)
echo "Test 3: Third message (conversation_depth=3)"
echo "Expected: Advanced frameworks ACTIVE (ACT/Schema/Narrative)"
echo "---"
RESP3=$(curl -s -X POST "$API_URL" \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"Everyone always leaves me in the end\", \"session_id\": \"$SESSION_ID\"}")

echo "$RESP3" | python3 -c "
import json, sys
d = json.load(sys.stdin)
print(f'✓ Emotion: {d.get(\"emotion\")}')
print(f'✓ Therapy mode: {d.get(\"therapy_mode\")}')
response = d.get('response', '')
print(f'✓ Response length: {len(response)} chars')
# Check if response contains framework-specific language
if 'schema' in response.lower() or 'pattern' in response.lower() or 'defusion' in response.lower():
    print('✅ Advanced framework language detected!')
else:
    print('⚠️  No advanced framework language (might be using basic CBT)')
print(f'  Preview: {response[:150]}...')
"
echo ""
sleep 1

# Test 4: Memory persistence check (new session, same user)
echo "Test 4: Session continuity test"
echo "Expected: Continuity prompt recognizing previous conversation"
echo "---"
RESP4=$(curl -s -X POST "$API_URL" \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"Hi, I am back\", \"session_id\": \"$SESSION_ID\"}")

echo "$RESP4" | python3 -c "
import json, sys
d = json.load(sys.stdin)
response = d.get('response', '')
print(f'✓ Response length: {len(response)} chars')
# Check for continuity language
if 'last time' in response.lower() or 'we talked' in response.lower() or 'remember' in response.lower():
    print('✅ Session continuity detected!')
else:
    print('⚠️  No continuity prompt (might be first message)')
print(f'  Response: {response[:200]}...')
"
echo ""

# Test 5: Check memory was saved
echo "Test 5: Verify memory persistence"
echo "---"
python3 << 'PYEOF'
import json
import os

cache_file = "data/memory_cache.json"
if os.path.exists(cache_file):
    with open(cache_file, 'r') as f:
        cache = json.load(f)

    total_users = len(cache)
    total_memories = sum(len(user_data.get('memories', [])) for user_data in cache.values())

    print(f'✓ Memory cache file exists')
    print(f'✓ Users stored: {total_users}')
    print(f'✓ Total memories: {total_memories}')

    if total_memories >= 3:
        print('✅ Memory system is working!')
    else:
        print('⚠️  Fewer memories than expected')
else:
    print('❌ Memory cache file not found!')
PYEOF
echo ""

# Test 6: Error handling - malformed request
echo "Test 6: Error handling - empty message"
echo "Expected: Graceful error response"
echo "---"
RESP_ERR=$(curl -s -X POST "$API_URL" \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"\", \"session_id\": \"$SESSION_ID\"}")

echo "$RESP_ERR" | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    if 'error' in d:
        print(f'✓ Error handled gracefully: {d.get(\"error\")}')
    else:
        print('⚠️  No error returned for empty message')
except:
    print('❌ Invalid JSON response')
"
echo ""

# Test 7: Check server logs for errors
echo "Test 7: Check server logs for errors"
echo "---"
if grep -i "error\|exception\|traceback" api_fresh_start.log | grep -v "print_exc" | head -5; then
    echo "⚠️  Errors found in logs (see above)"
else
    echo "✅ No errors in server logs"
fi
echo ""

echo "=========================================="
echo "🔴 RED TEAM TEST COMPLETE"
echo "=========================================="
