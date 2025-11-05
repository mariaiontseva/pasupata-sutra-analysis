#!/bin/bash
# Start local development environment for database-backed translation tool

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo "========================================"
echo "Sanskrit Translation Tool - Local Dev"
echo "========================================"

# Check Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo ""
    echo "[1/4] Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo ""
echo "[2/4] Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "[3/4] Installing dependencies..."
pip3 install -q --upgrade pip
pip3 install -q -r backend/requirements.txt

# Check if database exists
if [ ! -f "database/vivekamartanda.db" ]; then
    echo ""
    echo "⚠️  Database not found!"
    echo ""
    echo "Run migration script first:"
    echo "  python3 scripts/migrate_html_to_db.py"
    echo ""
    read -p "Run migration now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        python3 scripts/migrate_html_to_db.py
    else
        echo "Exiting. Run migration before starting server."
        exit 1
    fi
fi

# Check BeautifulSoup4 for migration script
if ! python3 -c "import bs4" 2>/dev/null; then
    echo ""
    echo "Installing beautifulsoup4 for HTML parsing..."
    pip3 install -q beautifulsoup4
fi

echo ""
echo "[4/4] Starting Flask API server..."
echo ""
echo "API will be available at: http://localhost:5000"
echo "Open index-local.html in your browser to use the tool"
echo ""
echo "Press Ctrl+C to stop the server"
echo "========================================"
echo ""

# Start Flask app
python3 backend/app.py
