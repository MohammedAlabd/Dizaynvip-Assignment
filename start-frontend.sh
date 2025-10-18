#!/bin/bash

# AI Chatbot Frontend Startup Script

echo "===================================="
echo "AI Chatbot Frontend - Startup Script"
echo "===================================="
echo ""

# Check if node_modules exists
if [ ! -d "frontend/node_modules" ]; then
    echo "📦 Installing dependencies..."
    cd frontend
    npm install
    cd ..
    echo "✅ Dependencies installed"
    echo ""
else
    cd frontend
fi

# Start Next.js development server
echo "🚀 Starting Next.js frontend server..."
echo "   URL: http://localhost:3000"
echo ""
npm run dev

