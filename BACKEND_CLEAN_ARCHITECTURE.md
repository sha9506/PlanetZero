# PlanetZero Backend - Clean Architecture

This is a **clean, production-ready backend** implementation focused solely on backend logic without external API integrations.

## 🏗️ Project Structure

```
backend/
├── main.py                    # FastAPI application entry point
├── database.py                # MongoDB connection management
├── requirements_new.txt       # Python dependencies
├── models/
│   └── __init__.py           # MongoDB document models
├── schemas/
│   └── __init__.py           # Pydantic request/response schemas
├── services/
│   ├── auth_service.py       # Authentication & JWT logic
│   ├── emission_service.py   # Carbon emission calculation
│   └── recommendation_service.py  # Recommendation generation
└── routes/
    ├── auth.py               # Authentication endpoints
    ├── consent.py            # Consent management
    ├── daily_log.py          # Daily emission logging
    ├── dashboard.py          # Dashboard summaries
    ├── history.py            # Emission history
    ├── leaderboard.py        # User rankings
    ├── recommendations.py    # Personalized recommendations
    └── profile.py            # User profile
```

## 📋 Features Implemented

### 1. **Authentication** (`routes/auth.py`)
- Email + password signup
- JWT-based authentication
- Secure password hashing with bcrypt
- Token-based session management

### 2. **Consent Management** (`routes/consent.py`)
- User consent storage
- Consent validation before data submission
- Fields: data_collection, data_usage, analytics

### 3. **Carbon Emission Calculation** (`services/emission_service.py`)

**Formula:** `Carbon Emission = Activity × Emission Factor`

#### Transportation
- Modes: car_petrol (0.192), car_diesel (0.171), bus (0.089), train (0.041), flight (0.255)
- Unit: kg CO₂ per km

#### Electricity
- Factor: 0.82 kg CO₂ per kWh (India average)

#### Food
- Types: veg (2.0), non_veg (5.5), vegan (1.5)
- Unit: kg CO₂ per meal

#### Lifestyle
- Categories: clothing (6.0), electronics (50.0)
- Unit: kg CO₂ per item

### 4. **Daily Logging** (`routes/daily_log.py`)
- Submit daily activities
- Automatic emission calculation
- Category-wise breakdown
- Update existing logs

### 5. **Dashboard** (`routes/dashboard.py`)
- Today's summary
- Weekly summary (last 7 days)
- Monthly summary (last 30 days)
- Highest emission category
- Average daily emissions

### 6. **History** (`routes/history.py`)
- Date-wise emission records
- Filterable by date range
- Sorted by date (newest first)

### 7. **Leaderboard** (`routes/leaderboard.py`)
- Ranking by lowest emissions
- Weekly, monthly, all-time periods
- User's rank and position
- Top performers list

### 8. **Recommendations** (`routes/recommendations.py`)

**Rule-Based Logic:**

**High Transportation →**
- Switch to public transport (45% savings)
- Carpool or bike (50% savings)
- Work from home (30% savings)

**High Electricity →**
- Optimize AC usage (35% savings)
- LED lighting (15% savings)
- Unplug devices (10% savings)

**High Food Emissions →**
- Plant-based meals (60% savings)
- Local & seasonal (25% savings)
- Reduce food waste (15% savings)

**High Lifestyle →**
- Buy second-hand (70% savings)
- Repair before replace (50% savings)
- Minimalist approach (40% savings)

### 9. **Profile Management** (`routes/profile.py`)
- View profile with statistics
- Update user information
- Emission analytics

## 🚀 API Endpoints

### Authentication
- `POST /api/auth/signup` - Register new user
- `POST /api/auth/login` - Login and get JWT token

### Consent
- `POST /api/consent` - Submit consent
- `GET /api/consent` - Get consent status

### Daily Log
- `POST /api/daily-log` - Submit daily emissions (requires consent)
- `GET /api/daily-log/{date}` - Get log for specific date

### Dashboard
- `GET /api/dashboard` - Get today, weekly, monthly summaries

### History
- `GET /api/history?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD&limit=30`

### Leaderboard
- `GET /api/leaderboard?period=monthly&limit=10`

### Recommendations
- `GET /api/recommendations` - Get personalized tips

### Profile
- `GET /api/profile` - Get user profile
- `PUT /api/profile` - Update profile

## 🔧 Setup Instructions

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements_new.txt
```

### 2. Configure Environment

Create `.env` file:

```env
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=planetzero
SECRET_KEY=your-secret-key-change-in-production
```

**Generate a secure SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 3. Start MongoDB

```bash
# macOS (Homebrew)
brew services start mongodb-community

# Linux (systemd)
sudo systemctl start mongod

# Or run manually
mongod --dbpath /path/to/data
```

### 4. Run the Application

```bash
python main.py
```

Or with uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Access API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 📊 Database Collections

### users
```json
{
  "_id": "ObjectId",
  "email": "user@example.com",
  "hashed_password": "bcrypt_hash",
  "name": "John Doe",
  "age": 25,
  "gender": "male",
  "country": "India",
  "city": "Mumbai",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z",
  "is_active": true
}
```

### consents
```json
{
  "_id": "ObjectId",
  "user_id": "user_ObjectId",
  "data_collection": true,
  "data_usage": true,
  "analytics": true,
  "consent_timestamp": "2024-01-01T00:00:00Z"
}
```

### daily_logs
```json
{
  "_id": "ObjectId",
  "user_id": "user_ObjectId",
  "date": "2024-01-01",
  "transportation": [
    {"mode": "car_petrol", "distance_km": 10}
  ],
  "electricity_kwh": 5.5,
  "food": [
    {"meal_type": "veg", "meals_count": 2}
  ],
  "lifestyle": [
    {"category": "clothing", "items_count": 1}
  ],
  "transport_emissions": 1.92,
  "electricity_emissions": 4.51,
  "food_emissions": 4.0,
  "lifestyle_emissions": 6.0,
  "total_emissions": 16.43,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

## 🧪 Testing

### Example: Create User and Log Emissions

```bash
# 1. Signup
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "name": "Test User"
  }'

# 2. Login
TOKEN=$(curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }' | jq -r '.access_token')

# 3. Submit Consent
curl -X POST http://localhost:8000/api/consent \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data_collection": true,
    "data_usage": true,
    "analytics": true
  }'

# 4. Log Daily Emissions
curl -X POST http://localhost:8000/api/daily-log \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2024-01-01",
    "transportation": [
      {"mode": "car_petrol", "distance_km": 10}
    ],
    "electricity_kwh": 5.5,
    "food": [
      {"meal_type": "veg", "meals_count": 2}
    ],
    "lifestyle": []
  }'

# 5. Get Dashboard
curl -X GET http://localhost:8000/api/dashboard \
  -H "Authorization: Bearer $TOKEN"
```

## 🔐 Security Features

- Passwords hashed with bcrypt
- JWT tokens for authentication
- Token expiration (7 days default)
- CORS protection
- Input validation with Pydantic
- SQL injection protection (using MongoDB)

## 📝 Code Quality

- Type hints throughout
- Comprehensive docstrings
- Separation of concerns
- Modular services
- Async/await for database operations
- Clean error handling

## 🎯 Production Readiness

✅ No external API dependencies  
✅ Environment-based configuration  
✅ Proper error handling  
✅ Structured logging ready  
✅ CORS configured  
✅ Database connection pooling  
✅ Secure authentication  
✅ Input validation  
✅ API documentation (Swagger/ReDoc)  

## 📦 Deployment Considerations

1. **Environment Variables**: Set in production
2. **MongoDB**: Use MongoDB Atlas or hosted instance
3. **Secret Key**: Generate strong random key
4. **CORS**: Update allowed origins
5. **HTTPS**: Use reverse proxy (nginx)
6. **Logging**: Configure production logging
7. **Monitoring**: Add health check monitoring

## 🔄 Integration with Frontend

The frontend React app should:

1. Store JWT token in localStorage
2. Include token in Authorization header
3. Handle 401 responses (logout)
4. Use proper date format (YYYY-MM-DD)
5. Validate inputs before submission

Example frontend API call:

```javascript
const token = localStorage.getItem('token');

const response = await fetch('http://localhost:8000/api/dashboard', {
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  }
});

const data = await response.json();
```

## 📄 License

This backend is built specifically for PlanetZero and follows clean architecture principles with no external dependencies beyond core functionality.
