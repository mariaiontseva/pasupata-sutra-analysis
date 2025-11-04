#!/bin/bash
# Start local development server for Pāśupata Sūtra Analysis

echo "🚀 Starting local web server..."
echo "📍 URL: http://localhost:8080"
echo "📝 Press Ctrl+C to stop"
echo ""

cd "$(dirname "$0")"
python3 -m http.server 8080
