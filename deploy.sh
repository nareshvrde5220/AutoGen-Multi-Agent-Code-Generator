#!/bin/bash

# Multi-Agent Framework Deployment Script
# This script builds and deploys the Multi-Agentic Coding Framework

set -e  # Exit on error

echo "=========================================="
echo "Multi-Agent Framework Deployment Script"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check if .env file exists
if [ ! -f "config/.env" ]; then
    print_warning ".env file not found. Creating from .env.example..."
    if [ -f "config/.env.example" ]; then
        cp config/.env.example config/.env
        print_status "Please edit config/.env with your actual API keys"
        exit 0
    else
        print_error ".env.example not found"
        exit 1
    fi
fi

# Load environment variables
print_status "Loading environment variables..."
set -a
source config/.env
set +a

# Check for required environment variables
if [ -z "$OPENAI_API_KEY" ] || [ "$OPENAI_API_KEY" == "your_openai_api_key_here" ]; then
    print_error "OPENAI_API_KEY not set in config/.env"
    exit 1
fi

# Create necessary directories
print_status "Creating necessary directories..."
mkdir -p output/generated_code
mkdir -p output/documentation
mkdir -p output/tests
mkdir -p logs

# Option 1: Docker deployment
deploy_docker() {
    print_status "Building Docker image..."
    docker-compose build

    print_status "Starting containers..."
    docker-compose up -d

    print_status "Waiting for service to be healthy..."
    sleep 10

    print_status "Checking container status..."
    docker-compose ps

    print_status "=========================================="
    print_status "Deployment complete!"
    print_status "Application is running at: http://localhost:8501"
    print_status "=========================================="

    print_status "To view logs: docker-compose logs -f"
    print_status "To stop: docker-compose down"
}

# Option 2: Local deployment
deploy_local() {
    print_status "Setting up Python virtual environment..."

    # Check if virtual environment exists
    if [ ! -d "genaivnv" ]; then
        print_status "Creating virtual environment..."
        python -m venv genaivnv
    fi

    # Activate virtual environment
    print_status "Activating virtual environment..."
    if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        source genaivnv/Scripts/activate
    else
        source genaivnv/bin/activate
    fi

    print_status "Installing dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt

    print_status "Starting Streamlit application..."
    print_status "=========================================="
    print_status "Application starting at: http://localhost:8501"
    print_status "=========================================="
    
    streamlit run ui/streamlit_app.py
}

# Option 3: Run tests
run_tests() {
    print_status "Running tests..."

    # Activate virtual environment if it exists
    if [ -d "genaivnv" ]; then
        if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
            source genaivnv/Scripts/activate
        else
            source genaivnv/bin/activate
        fi
    fi

    pytest tests/ -v --tb=short

    print_status "Tests completed!"
}

# Main menu
echo ""
echo "Select deployment option:"
echo "1) Deploy with Docker"
echo "2) Deploy locally (requires Python 3.10+)"
echo "3) Run tests"
echo "4) Exit"
echo ""
read -p "Enter option (1-4): " option

case $option in
    1)
        deploy_docker
        ;;
    2)
        deploy_local
        ;;
    3)
        run_tests
        ;;
    4)
        print_status "Exiting..."
        exit 0
        ;;
    *)
        print_error "Invalid option"
        exit 1
        ;;
esac
