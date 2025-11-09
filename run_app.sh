#!/bin/bash

# Script to run Flask app and handle port conflicts
# Usage: bash run_app.sh

echo "=== Starting Flask App ==="

# Kill any existing processes on port 5000
if lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null ; then
    echo "Port 5000 is in use. Killing existing processes..."
    lsof -ti:5000 | xargs kill -9
    sleep 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Start Flask app
echo "Starting Flask on http://127.0.0.1:5000"
echo "Press CTRL+C to stop"
echo ""
python app.py
