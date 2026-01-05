# 🚀 PlanetZero Quick Start Guide

This guide will help you get PlanetZero running on your local machine in minutes.

## ⚡ Super Quick Start (Automated)

If you have MongoDB installed and running:

```bash
./start-dev.sh
```

This script will:
- Set up Python virtual environment
- Install all dependencies
- Initialize the database
- Start both backend and frontend servers

## 📋 Step-by-Step Setup

### Step 1: Install Prerequisites

**macOS:**
```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Node.js
brew install node

# Install Python
brew install python@3.11

# Install MongoDB
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

**Linux (Ubuntu/Debian):**
```bash
# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install Python
sudo apt-get install python3 python3-pip python3-venv

# Install MongoDB
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org
sudo systemctl start mongod
```

**Windows:**
- Download and install [Node.js](https://nodejs.org/)
- Download and install [Python](https://www.python.org/downloads/)
- Download and install [MongoDB Community Server](https://www.mongodb.com/try/download/community)

### Step 2: Clone Repository

```bash
git clone https://github.com/sha9506/PlanetZero.git
cd PlanetZero
```

### Step 3: Setup Backend

```bash
# Navigate to backend
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env

# Edit .env file (optional - defaults work for local MongoDB)
nano .env  # or use any text editor

# Initialize database
python init_db.py

# Start backend server
python main.py
```

Backend will be running at: **http://localhost:8000**

### Step 4: Setup Frontend (New Terminal)

```bash
# Navigate to frontend directory
cd PlanetZero/frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env

# Start React development server
npm start
```

Frontend will be running at: **http://localhost:3000**

## ✅ Verify Installation

1. **Check Backend**: Visit http://localhost:8000/docs
   - You should see the FastAPI Swagger documentation

2. **Check Frontend**: Visit http://localhost:3000
   - You should see the PlanetZero landing page

3. **Test Full Flow**:
   - Click "Get Started"
   - Sign up with email and password
   - Complete onboarding
   - Log a daily activity
   - Check the leaderboard

## 🔍 Troubleshooting

### MongoDB Connection Error

**Error**: `Could not connect to MongoDB`

**Solution**:
```bash
# Check if MongoDB is running
# macOS:
brew services list | grep mongodb

# Linux:
sudo systemctl status mongod

# Start MongoDB if not running
# macOS:
brew services start mongodb-community

# Linux:
sudo systemctl start mongod
```

### Port Already in Use

**Error**: `Port 8000 is already in use`

**Solution**:
```bash
# Find and kill process using port 8000
lsof -ti:8000 | xargs kill -9

# Or change port in backend/.env
PORT=8001
```

### Python Dependencies Error

**Error**: `No module named 'fastapi'`

**Solution**:
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### React Build Error

**Error**: `npm ERR! missing script: start`

**Solution**:
```bash
# Make sure you're in the project root, not backend folder
cd ..

# Install dependencies
npm install

# Try again
npm start
```

## 🎯 Quick Test API

Once both servers are running, test the API:

```bash
# Sign up a user
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123",
    "name": "Test User"
  }'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=testpass123"
```

## 📚 Next Steps

1. **Explore the API**: http://localhost:8000/docs
2. **Create your profile**: Complete the onboarding flow
3. **Log activities**: Track your daily carbon footprint
4. **Join communities**: Find like-minded individuals
5. **Earn badges**: Complete recommendations and challenges

## 🛠️ Development Tips

### Hot Reload

Both servers support hot reload:
- **Backend**: Changes to `.py` files auto-reload
- **Frontend**: Changes to `.jsx/.css` files auto-reload

### API Testing

Use the built-in Swagger UI for API testing:
- http://localhost:8000/docs

### Database Management

View your MongoDB data:
```bash
# Connect to MongoDB shell
mongosh

# Switch to database
use planetzero

# View collections
show collections

# Query users
db.users.find().pretty()
```

### VS Code Extensions (Recommended)

- Python
- Pylance
- ES7+ React/Redux/React-Native snippets
- MongoDB for VS Code
- REST Client

## 🐛 Getting Help

If you encounter issues:

1. Check the [Backend README](backend/README.md) for detailed API documentation
2. Look at the terminal output for error messages
3. Check MongoDB is running: `brew services list` (macOS)
4. Verify ports 3000 and 8000 are available
5. Create an issue on GitHub with error details

---

**Happy Coding! 🌍💚**
