#!/bin/bash

# PlanetZero Backend - Setup Script
# This script sets up the clean backend architecture

echo "🌍 PlanetZero Backend Setup"
echo "============================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python found:${NC} $(python3 --version)"

# Check if MongoDB is running
if ! pgrep -x "mongod" > /dev/null; then
    echo -e "${YELLOW}Warning: MongoDB is not running${NC}"
    echo "Please start MongoDB first:"
    echo "  macOS: brew services start mongodb-community"
    echo "  Linux: sudo systemctl start mongod"
    echo ""
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${GREEN}✓ Virtual environment already exists${NC}"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies from requirements_new.txt..."
pip install -r requirements_new.txt

echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Warning: .env file not found${NC}"
    echo "Creating .env file..."
    
    # Generate secret key
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
    
    cat > .env << EOF
# MongoDB Configuration
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=planetzero

# JWT Secret Key (DO NOT SHARE)
SECRET_KEY=${SECRET_KEY}

# CORS Origins
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001
EOF
    
    echo -e "${GREEN}✓ .env file created with secure SECRET_KEY${NC}"
else
    echo -e "${GREEN}✓ .env file already exists${NC}"
fi

echo ""
echo "============================"
echo -e "${GREEN}Setup Complete!${NC}"
echo "============================"
echo ""
echo "To start the backend server:"
echo "  1. Ensure MongoDB is running"
echo "  2. Run: python main.py"
echo ""
echo "API will be available at:"
echo "  - http://localhost:8000"
echo "  - Docs: http://localhost:8000/docs"
echo "  - ReDoc: http://localhost:8000/redoc"
echo ""
