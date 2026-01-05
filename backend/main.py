"""
PlanetZero Backend API
FastAPI application for carbon emission tracking and sustainability

Main Features:
- User authentication with JWT
- Consent management
- Daily emission logging with automatic calculation
- Dashboard with period-wise summaries
- Emission history
- Leaderboard
- Personalized recommendations
- User profile management
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
from dotenv import load_dotenv
import os

from database import connect_to_mongo, close_mongo_connection

# Import routers
from routes import (
    auth,
    consent,
    daily_log,
    dashboard,
    history,
    leaderboard,
    recommendations,
    profile,
    charts
)

# Load environment variables
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager
    Handles startup and shutdown events
    """
    # Startup
    print("🌍 Starting PlanetZero Backend...")
    await connect_to_mongo()
    yield
    # Shutdown
    print("👋 Shutting down PlanetZero Backend...")
    await close_mongo_connection()

# Initialize FastAPI app
app = FastAPI(
    title="PlanetZero API",
    description="Backend API for carbon emission tracking and sustainability",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:3001").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers with /api prefix
app.include_router(auth.router, prefix="/api")
app.include_router(consent.router, prefix="/api")
app.include_router(daily_log.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")
app.include_router(history.router, prefix="/api")
app.include_router(leaderboard.router, prefix="/api")
app.include_router(recommendations.router, prefix="/api")
app.include_router(profile.router, prefix="/api")
app.include_router(charts.router, prefix="/api")

@app.get("/")
async def root():
    """
    Root endpoint - API information
    """
    return {
        "message": "Welcome to PlanetZero API",
        "version": "1.0.0",
        "description": "Carbon emission tracking and sustainability platform",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health",
        "endpoints": {
            "authentication": "/api/auth",
            "consent": "/api/consent",
            "daily_log": "/api/daily-log",
            "dashboard": "/api/dashboard",
            "history": "/api/history",
            "leaderboard": "/api/leaderboard",
            "recommendations": "/api/recommendations",
            "profile": "/api/profile",
            "charts": "/api/charts"
        }
    }

@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring
    """
    return {
        "status": "healthy",
        "service": "planetzero-backend",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("DEBUG", "True") == "True",
        log_level="info"
    )
