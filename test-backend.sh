#!/bin/bash

# AI Chatbot Backend Test Script

echo "==================================="
echo "AI Chatbot Backend - Test Script"
echo "==================================="
echo ""

# Check if .env file exists
if [ ! -f "backend/.env" ]; then
    echo "❌ Error: .env file not found in backend directory!"
    echo ""
    echo "Please create a .env file with your OpenAI API key:"
    echo "  cd backend"
    echo "  cp env.template .env"
    echo "  # Edit .env and add your OpenAI API key"
    echo ""
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "backend/venv" ]; then
    echo "📦 Creating virtual environment..."
    cd backend
    python3 -m venv venv
    cd ..
    echo "✅ Virtual environment created"
    echo ""
fi

# Activate virtual environment and install dependencies
echo "📦 Installing/updating dependencies..."
cd backend
source venv/bin/activate

# Check if requirements are installed
pip install -q -r requirements.txt

echo "✅ Dependencies ready"
echo ""

# Run the test
echo "🧪 Running backend tests..."
echo ""
python test_chatbot.py

