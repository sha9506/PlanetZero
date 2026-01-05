#!/bin/bash

# PlanetZero - Development Setup Script
# This script sets up and runs both frontend and backend

echo "PlanetZero Development Setup"
echo "================================"

# Check if MongoDB is running
echo ""
echo "Checking MongoDB..."
if ! pgrep -x "mongod" > /dev/null; then
    echo "WARNING: MongoDB is not running!"
    echo "Start MongoDB with: brew services start mongodb-community"
    echo "Or use MongoDB Atlas (cloud) and update backend/.env"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "MongoDB is running"
fi

# Backend Setup
echo ""
echo "Setting up Backend..."
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt > /dev/null 2>&1

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "WARNING: No .env file found!"
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo "Please update .env with your configuration"
fi

# Initialize database
echo "Initializing database with badges..."
python init_db.py

# Start backend server in background
echo "Starting FastAPI backend..."
python main.py > /dev/null 2>&1 &
BACKEND_PID=$!
echo "Backend running on http://localhost:8000 (PID: $BACKEND_PID)"

cd ..

# Frontend Setup
echo ""
echo "Setting up Frontend..."
cd ../frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing npm dependencies..."
    npm install
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "WARNING: No .env file found!"
    echo "Creating .env from .env.example..."
    cp .env.example .env
fi

# Start frontend server
echo "Starting React frontend..."
npm start &
FRONTEND_PID=$!

echo ""
echo "================================"
echo "PlanetZero is running!"
echo ""
echo "Frontend: http://localhost:3000"
echo "Backend:  http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both servers"
echo "================================"

# Wait for Ctrl+C
trap "echo ''; echo 'Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT

# Keep script running
wait
