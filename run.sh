#!/bin/bash
# Quick launcher for Multi-Agent Framework Streamlit UI

echo "=========================================="
echo "Multi-Agent Framework - Quick Launcher"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -f "genaivnv/bin/activate" ]; then
    echo "[ERROR] Virtual environment not found!"
    echo "Please run deploy.sh first to set up the environment."
    exit 1
fi

# Activate virtual environment
source genaivnv/bin/activate

# Check if .env file exists
if [ ! -f "config/.env" ]; then
    echo "[WARNING] Configuration file not found!"
    echo ""
    echo "Creating config/.env from template..."
    cp config/.env.example config/.env
    echo ""
    echo "IMPORTANT: Please edit config/.env and add your OpenAI API key"
    echo "Then run this script again."
    echo ""
    exit 0
fi

# Launch Streamlit
echo "Starting Streamlit application..."
echo ""
echo "=========================================="
echo "Application will open at: http://localhost:8501"
echo "Press Ctrl+C to stop the server"
echo "=========================================="
echo ""

streamlit run ui/streamlit_app.py
