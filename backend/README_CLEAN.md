# Clean Backend Architecture for PlanetZero

This directory contains a **clean, production-ready backend** implementation with the following structure:

## 🗂️ File Structure

```
backend/
├── main.py                    # FastAPI application entry point
├── database.py                # MongoDB connection
├── requirements_new.txt       # Clean dependencies list
├── setup_clean.sh            # Setup script
│
├── models/
│   └── __init__.py           # MongoDB document models
│
├── schemas/
│   └── __init__.py           # Pydantic request/response schemas
│
├── services/
│   ├── auth_service.py       # Authentication & JWT
│   ├── emission_service.py   # Carbon calculation
│   └── recommendation_service.py  # Recommendations
│
└── routes/
    ├── auth.py               # POST /api/auth/signup, /api/auth/login
    ├── consent.py            # POST/GET /api/consent
    ├── daily_log.py          # POST/GET /api/daily-log
    ├── dashboard.py          # GET /api/dashboard
    ├── history.py            # GET /api/history
    ├── leaderboard.py        # GET /api/leaderboard
    ├── recommendations.py    # GET /api/recommendations
    └── profile.py            # GET/PUT /api/profile
```

## 🚀 Quick Start

### 1. Setup

```bash
cd backend
chmod +x setup_clean.sh
./setup_clean.sh
```

This will:
- Create virtual environment
- Install dependencies
- Generate secure SECRET_KEY
- Create .env file

### 2. Start Server

```bash
python main.py
```

Or with uvicorn directly:

```bash
uvicorn main:app --reload
```

### 3. Access API

- API: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 📋 Key Features

### ✅ Implemented

1. **Authentication**
   - Email + password signup
   - JWT-based login
   - Secure password hashing

2. **Consent Management**
   - Store user consent
   - Validate before data submission

3. **Carbon Calculation**
   - Transportation (car, bus, train, flight)
   - Electricity (kWh)
   - Food (veg, non-veg, vegan)
   - Lifestyle (clothing, electronics)

4. **Daily Logging**
   - Submit daily activities
   - Automatic emission calculation
   - Category-wise breakdown

5. **Dashboard**
   - Today/Weekly/Monthly summaries
   - Highest emission category
   - Average daily emissions

6. **History**
   - Date-wise records
   - Date range filtering

7. **Leaderboard**
   - Rank users by lowest emissions
   - Weekly/Monthly/All-time

8. **Recommendations**
   - Rule-based suggestions
   - Potential carbon savings
   - Category-specific tips

9. **Profile**
   - View/Update user info
   - Emission statistics

### ❌ NOT Included (As Per Requirements)

- ❌ External API integrations
- ❌ Social login
- ❌ Frontend code
- ❌ Deployment configs

## 🧪 Testing

```bash
# 1. Signup
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "test123", "name": "Test User"}'

# 2. Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "test123"}'

# 3. Submit Consent (use token from login)
curl -X POST http://localhost:8000/api/consent \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"data_collection": true, "data_usage": true, "analytics": true}'

# 4. Log Daily Emissions
curl -X POST http://localhost:8000/api/daily-log \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2024-01-01",
    "transportation": [{"mode": "car_petrol", "distance_km": 10}],
    "electricity_kwh": 5.5,
    "food": [{"meal_type": "veg", "meals_count": 2}],
    "lifestyle": []
  }'
```

## 📊 Emission Factors

### Transportation (kg CO₂/km)
- Car Petrol: 0.192
- Car Diesel: 0.171
- Bus: 0.089
- Train: 0.041
- Flight: 0.255

### Electricity
- 0.82 kg CO₂/kWh (India average)

### Food (kg CO₂/meal)
- Vegetarian: 2.0
- Non-vegetarian: 5.5
- Vegan: 1.5

### Lifestyle (kg CO₂/item)
- Clothing: 6.0
- Electronics: 50.0

## 🔒 Security

- Bcrypt password hashing
- JWT token authentication
- Token expiration (7 days)
- CORS protection
- Input validation
- MongoDB injection protection

## 📚 Documentation

See `BACKEND_CLEAN_ARCHITECTURE.md` for detailed documentation.

## 🐛 Troubleshooting

**MongoDB connection error:**
```bash
# Start MongoDB
brew services start mongodb-community  # macOS
sudo systemctl start mongod            # Linux
```

**Import errors:**
```bash
# Ensure you're in virtual environment
source venv/bin/activate
pip install -r requirements_new.txt
```

**Port 8000 already in use:**
```bash
# Kill existing process
lsof -ti:8000 | xargs kill -9
```

## 📝 Notes

- This is a **clean implementation** focused on backend logic only
- Single unified `main.py` file
- All dependencies in `requirements_new.txt`
- Self-contained with no external API dependencies
- Ready for production deployment
