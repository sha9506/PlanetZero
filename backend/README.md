# PlanetZero Backend API

FastAPI-based backend for PlanetZero carbon footprint tracking platform with MongoDB database.

## 🚀 Features

- **User Authentication**: JWT-based authentication with secure password hashing
- **Daily Activity Logging**: Track transport, energy, and meal activities with automatic carbon calculation
- **Recommendations System**: Personalized eco-friendly recommendations
- **Community Platform**: Create and join communities with role-based access
- **Leaderboard**: Real-time rankings based on points and emissions
- **Notifications**: Achievement and activity notifications
- **Badge System**: Gamification with 9 different badges

## 📋 Prerequisites

- Python 3.8+
- MongoDB 4.4+ (local or cloud instance)
- pip (Python package manager)

## 🛠️ Installation

### 1. Clone the repository

```bash
cd backend
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate  # On Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env` and update the values:

```bash
cp .env.example .env
```

Edit `.env`:

```env
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=planetzero
SECRET_KEY=your-super-secret-key-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALLOWED_ORIGINS=http://localhost:3000
DEBUG=True
HOST=0.0.0.0
PORT=8000
```

### 5. Start MongoDB

Make sure MongoDB is running:

```bash
# macOS (if installed via Homebrew)
brew services start mongodb-community

# Linux
sudo systemctl start mongod

# Or use MongoDB Atlas (cloud) and update MONGODB_URL
```

### 6. Initialize database with badges

```bash
python init_db.py
```

### 7. Start the server

```bash
python main.py
```

Or with uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

## 📚 API Documentation

Once the server is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔐 Authentication Flow

1. **Sign Up**: `POST /api/auth/signup`
   ```json
   {
     "email": "user@example.com",
     "password": "securepassword",
     "name": "John Doe"
   }
   ```

2. **Login**: `POST /api/auth/login`
   ```json
   {
     "username": "user@example.com",
     "password": "securepassword"
   }
   ```
   Returns JWT token

3. **Use Token**: Include in headers for protected routes:
   ```
   Authorization: Bearer <access_token>
   ```

## 🛣️ API Routes

### Authentication (`/api/auth`)
- `POST /signup` - Register new user
- `POST /login` - Login and get JWT token
- `POST /consent` - Accept data consent

### Users (`/api/users`)
- `GET /me` - Get current user profile
- `PUT /me` - Update user profile
- `POST /onboarding` - Complete onboarding
- `GET /{user_id}` - Get user by ID

### Activities (`/api/activities`)
- `POST /daily-logs` - Create daily log
- `GET /daily-logs` - Get user's daily logs
- `GET /daily-logs/{log_id}` - Get specific log
- `PUT /daily-logs/{log_id}` - Update daily log
- `DELETE /daily-logs/{log_id}` - Delete daily log
- `GET /stats` - Get activity statistics

### Recommendations (`/api/recommendations`)
- `GET /` - Get all recommendations
- `GET /{recommendation_id}` - Get specific recommendation
- `POST /{recommendation_id}/complete` - Mark as completed
- `POST /{recommendation_id}/uncomplete` - Mark as not completed
- `GET /user/completed` - Get user's completed recommendations

### Communities (`/api/communities`)
- `POST /` - Create community
- `GET /` - Get all communities (with filters)
- `GET /my-communities` - Get user's communities
- `GET /{community_id}` - Get specific community
- `POST /{community_id}/join` - Join community
- `POST /{community_id}/leave` - Leave community
- `GET /{community_id}/members` - Get community members
- `PUT /{community_id}/activities` - Update activities (leaders only)

### Leaderboard (`/api/leaderboard`)
- `GET /` - Get leaderboard rankings
- `GET /user/{user_id}` - Get user's rank
- `GET /stats` - Get leaderboard statistics

### Notifications (`/api/notifications`)
- `GET /` - Get user's notifications
- `GET /unread-count` - Get unread count
- `PUT /{notification_id}/read` - Mark as read
- `PUT /read-all` - Mark all as read
- `DELETE /{notification_id}` - Delete notification

## 🧮 Carbon Calculation

### Emission Factors

**Transport (kg CO2 per km)**:
- Car (Gasoline): 0.21
- Car (Diesel): 0.17
- Car (Electric): 0.05
- Car (Hybrid): 0.12
- Bus: 0.08
- Train: 0.04
- Subway/Metro: 0.03
- Bicycle: 0.0
- Walking: 0.0
- Motorcycle: 0.15
- Flight: 0.25

**Energy**: 0.5 kg CO2 per kWh

**Meals**: 2.0 kg CO2 per serving (average)

## 📊 Database Collections

- **users**: User accounts and profiles
- **daily_logs**: Daily activity logs
- **recommendations**: Eco-friendly recommendations
- **communities**: Community information
- **community_members**: Community membership and roles
- **badges**: Available badges
- **user_badges**: Badges earned by users
- **notifications**: User notifications

## 🎯 Points System

- Daily log creation: +10 points
- Recommendation completion: +50 points
- Community join: +25 points

## 🏆 Badges

1. **First Steps** (Gold) - Log first activity
2. **Week Warrior** (Green) - 7-day streak
3. **Eco Champion** (Blue) - 20% emission reduction
4. **Green Commuter** (Purple) - 10 public transport uses
5. **Energy Saver** (Orange) - 30% energy reduction
6. **Zero Waste Hero** (Teal) - 5 recycling tasks
7. **Team Player** (Pink) - Join 3 communities
8. **100-Day Streak** (Indigo) - 100-day logging streak
9. **Community Founder** (Emerald) - Create a community

## 🔧 Development

### Project Structure

```
backend/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── init_db.py             # Database initialization script
├── app/
│   ├── __init__.py
│   ├── database.py        # MongoDB connection
│   ├── models.py          # Pydantic models
│   ├── auth.py            # Authentication utilities
│   └── routes/
│       ├── __init__.py
│       ├── auth.py        # Auth endpoints
│       ├── users.py       # User endpoints
│       ├── activities.py  # Activity endpoints
│       ├── recommendations.py
│       ├── communities.py
│       ├── leaderboard.py
│       └── notifications.py
```

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

## 🐳 Docker Deployment (Optional)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
docker build -t planetzero-api .
docker run -p 8000:8000 --env-file .env planetzero-api
```

## 📝 License

MIT License

## 👤 Author

**Shabnam Hazari**
- GitHub: [@sha9506](https://github.com/sha9506)

---

**Happy Coding! 🌍💚**
