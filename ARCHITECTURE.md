# 🏗️ PlanetZero Architecture

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                             │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    React Frontend                         │  │
│  │                   (Port 3000)                             │  │
│  │                                                            │  │
│  │  Components:                                              │  │
│  │  • Navbar • Footer                                        │  │
│  │  • EmissionCard • ChartCard • RecommendationCard         │  │
│  │                                                            │  │
│  │  Pages:                                                    │  │
│  │  • Landing • Intro • Login/Signup                         │  │
│  │  • Dashboard • DailyLog • History                         │  │
│  │  • Recommendations • Community                            │  │
│  │  • Leaderboard • Profile                                  │  │
│  │                                                            │  │
│  │  Context:                                                  │  │
│  │  • UserContext (Authentication State)                     │  │
│  │                                                            │  │
│  │  Services:                                                 │  │
│  │  • api.js (HTTP Client)                                   │  │
│  └────────────────────┬─────────────────────────────────────┘  │
│                       │ HTTP/REST (JSON)                        │
│                       │ JWT Bearer Token                         │
└───────────────────────┼─────────────────────────────────────────┘
                        │
                        │ CORS Enabled
                        │
┌───────────────────────▼─────────────────────────────────────────┐
│                      API GATEWAY LAYER                           │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              FastAPI Backend                              │  │
│  │              (Port 8000)                                  │  │
│  │                                                            │  │
│  │  Middleware:                                              │  │
│  │  • CORS • Authentication (JWT)                           │  │
│  │                                                            │  │
│  │  Routes:                                                   │  │
│  │  ┌─────────────────────────────────────────────────┐    │  │
│  │  │ /api/auth          - Authentication             │    │  │
│  │  │ /api/users         - User Management            │    │  │
│  │  │ /api/activities    - Daily Logs & Stats         │    │  │
│  │  │ /api/recommendations - Eco Suggestions          │    │  │
│  │  │ /api/communities   - Community Platform         │    │  │
│  │  │ /api/leaderboard   - Rankings & Badges          │    │  │
│  │  │ /api/notifications - User Notifications         │    │  │
│  │  └─────────────────────────────────────────────────┘    │  │
│  │                                                            │  │
│  │  Auto-Generated Docs:                                     │  │
│  │  • /docs (Swagger UI)                                     │  │
│  │  • /redoc (ReDoc)                                         │  │
│  └────────────────────┬─────────────────────────────────────┘  │
└───────────────────────┼─────────────────────────────────────────┘
                        │
                        │ Motor (Async Driver)
                        │
┌───────────────────────▼─────────────────────────────────────────┐
│                    DATABASE LAYER                                │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                  MongoDB                                  │  │
│  │              (Port 27017)                                 │  │
│  │                                                            │  │
│  │  Database: planetzero                                     │  │
│  │                                                            │  │
│  │  Collections:                                             │  │
│  │  ┌────────────────────────────────────────────────┐      │  │
│  │  │ users              - User accounts & profiles  │      │  │
│  │  │ daily_logs         - Activity tracking         │      │  │
│  │  │ recommendations    - Eco suggestions (10)      │      │  │
│  │  │ communities        - Community groups          │      │  │
│  │  │ community_members  - Membership & roles        │      │  │
│  │  │ badges             - Achievement badges (9)    │      │  │
│  │  │ user_badges        - Earned achievements       │      │  │
│  │  │ notifications      - User notifications        │      │  │
│  │  └────────────────────────────────────────────────┘      │  │
│  └──────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Authentication Flow

```
User → React Login Form
  ↓
  POST /api/auth/login (OAuth2 Form Data)
  ↓
FastAPI Auth Route
  ↓
Verify Password (bcrypt)
  ↓
Generate JWT Token
  ↓
Return {access_token, token_type}
  ↓
Store in localStorage
  ↓
Include in all requests: Authorization: Bearer {token}
```

### 2. Daily Log Creation Flow

```
User fills Daily Log form
  ↓
  POST /api/activities/daily-logs
  ↓
FastAPI validates JWT
  ↓
Calculate Carbon Footprint:
  - Transport: Σ(distance × emission_factor)
  - Energy: (electricity + heating) × 0.5
  - Meals: count × 2.0
  ↓
Save to MongoDB (daily_logs collection)
  ↓
Update user's total_emissions
  ↓
Award 10 points
  ↓
Create milestone notification
  ↓
Return created log with carbon_footprint
```

### 3. Community Creation Flow

```
User creates community
  ↓
  POST /api/communities
  ↓
FastAPI validates JWT
  ↓
Save community to MongoDB
  ↓
Add user as "Community Leader" member
  ↓
Check for "Community Founder" badge
  ↓
Award badge (if first community)
  ↓
Update user's badges array
  ↓
Create achievement notification
  ↓
Return created community
```

### 4. Recommendation Completion Flow

```
User marks recommendation complete
  ↓
  POST /api/recommendations/{id}/complete
  ↓
FastAPI validates JWT
  ↓
Check if already completed
  ↓
Add to user's completed_recommendations array
  ↓
Award 50 points
  ↓
Create achievement notification
  ↓
Return success with points_awarded
```

## Technology Stack Detail

### Frontend
```
React 18.x
  ├── react-router-dom (Routing)
  ├── react-icons (Font Awesome icons)
  └── Custom CSS (No framework)

State Management:
  ├── useState (Local state)
  ├── useEffect (Side effects)
  └── Context API (User authentication)
```

### Backend
```
FastAPI 0.109.0
  ├── Uvicorn (ASGI Server)
  ├── Pydantic (Data validation)
  ├── python-jose (JWT)
  ├── passlib[bcrypt] (Password hashing)
  ├── Motor 3.3.2 (Async MongoDB driver)
  └── python-dotenv (Environment variables)
```

### Database
```
MongoDB
  ├── Collections: 8
  ├── Documents: Dynamic
  ├── Indexes: _id (default)
  └── Schema: Flexible (NoSQL)
```

## Security Features

1. **Password Security**
   - Bcrypt hashing (cost factor: default)
   - Passwords never stored in plain text

2. **JWT Authentication**
   - HS256 algorithm
   - 30-minute expiration
   - Token stored in localStorage

3. **CORS Configuration**
   - Allowed origins: localhost:3000
   - Credentials: enabled
   - Methods: all
   - Headers: all

4. **Input Validation**
   - Pydantic models for request validation
   - Email validation
   - Enum validation for categories

## API Response Format

### Success Response
```json
{
  "id": "unique_id",
  "field1": "value1",
  "field2": "value2",
  ...
}
```

### Error Response
```json
{
  "detail": "Error message description"
}
```

### List Response
```json
[
  {object1},
  {object2},
  ...
]
```

## Environment Variables

### Frontend (frontend/.env)
```
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_ENV=development
REACT_APP_ENABLE_AUTH=true
REACT_APP_ENABLE_COMMUNITIES=true
REACT_APP_ENABLE_NOTIFICATIONS=true
```

### Backend (backend/.env)
```
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=planetzero
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALLOWED_ORIGINS=http://localhost:3000
DEBUG=True
HOST=0.0.0.0
PORT=8000
```

## Deployment Architecture (Future)

```
┌──────────────────────────────────────────────────┐
│              Production Environment               │
│                                                    │
│  Vercel/Netlify (Frontend)                       │
│       ↓                                            │
│  API Gateway / Load Balancer                      │
│       ↓                                            │
│  Docker Container (FastAPI)                       │
│       ↓                                            │
│  MongoDB Atlas (Cloud Database)                   │
│       ↓                                            │
│  Redis Cache (Future)                             │
│       ↓                                            │
│  CloudWatch / Logging Service                     │
└──────────────────────────────────────────────────┘
```

## Scalability Considerations

1. **Database Indexing**
   - User email (unique)
   - User points (for leaderboard)
   - Community category (for filtering)
   - Notification user_id + read status

2. **Caching Strategy** (Future)
   - Leaderboard rankings (Redis)
   - Recommendations list (15-minute TTL)
   - Community lists (5-minute TTL)

3. **Rate Limiting** (Future)
   - 100 requests/minute per user
   - 1000 requests/hour per IP

4. **Horizontal Scaling**
   - Stateless API design
   - JWT tokens (no session storage)
   - MongoDB replica sets
   - Load balancer ready

---

**Architecture designed for scalability, security, and maintainability!** 🏗️
