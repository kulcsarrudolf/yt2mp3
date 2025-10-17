#!/bin/bash
# Functional test for ytmp3 - Downloads a 5 second clip

set -e

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║            ytmp3 Functional Test (5 sec clip)                ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check if ytmp3 is available
if ! command -v ytmp3 &> /dev/null; then
    echo "❌ ytmp3 is not installed. Please install it first:"
    echo "   uv pip install -e ."
    exit 1
fi

# Test video URL (public domain)
TEST_URL="https://www.youtube.com/watch?v=jNQXAC9IVRw"  # "Me at the zoo" - first YouTube video
TEST_OUTPUT="/tmp/ytmp3_test"
TIMESTAMP=$(date +%s)

echo "🎵 Test Configuration:"
echo "   URL: $TEST_URL"
echo "   Clip: 5 seconds (from 0:01 to 0:06)"
echo "   Output: ${TEST_OUTPUT}_${TIMESTAMP}.mp3"
echo ""

echo "📥 Running ytmp3..."
echo "   Command: ytmp3 --url \"$TEST_URL\" --start-time 1 --duration 5 --output-dir /tmp --filename ytmp3_test_${TIMESTAMP} --quality 128 --quiet"
echo ""

# Run the actual test
if ytmp3 --url "$TEST_URL" \
         --start-time 1 \
         --duration 5 \
         --output-dir /tmp \
         --filename "ytmp3_test_${TIMESTAMP}" \
         --quality 128 \
         --quiet 2>&1; then
    
    OUTPUT_FILE="${TEST_OUTPUT}_${TIMESTAMP}.mp3"
    
    if [ -f "$OUTPUT_FILE" ]; then
        SIZE=$(du -h "$OUTPUT_FILE" | cut -f1)
        echo "✅ Success! File downloaded: $OUTPUT_FILE"
        echo "   Size: $SIZE"
        echo ""
        
        # Check duration with ffprobe if available
        if command -v ffprobe &> /dev/null; then
            DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$OUTPUT_FILE" 2>/dev/null | awk '{print int($1)}')
            echo "   Duration: ${DURATION} seconds"
        fi
        
        echo ""
        echo "🧹 Cleaning up test file..."
        rm -f "$OUTPUT_FILE"
        echo "✓ Cleanup complete"
    else
        echo "❌ Test failed: Output file not created"
        exit 1
    fi
else
    echo "❌ Test failed: ytmp3 command failed"
    exit 1
fi

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║         ✅ Functional Test Passed!                           ║"
echo "╚══════════════════════════════════════════════════════════════╝"

