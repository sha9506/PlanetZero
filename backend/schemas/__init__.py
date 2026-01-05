"""
Pydantic Schemas for Request/Response Validation
These schemas validate incoming API requests and outgoing responses
"""
from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel, EmailStr, Field, validator

# ============ Authentication Schemas ============

class SignupRequest(BaseModel):
    """Schema for user signup request"""
    email: EmailStr
    password: str = Field(..., min_length=6)
    name: str = Field(..., min_length=2)
    age: Optional[int] = Field(None, ge=1, le=150)
    gender: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters')
        return v

class LoginRequest(BaseModel):
    """Schema for user login request"""
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    """Schema for JWT token response"""
    access_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    """Schema for user data response"""
    id: str
    email: str
    name: str
    age: Optional[int]
    gender: Optional[str]
    country: Optional[str]
    city: Optional[str]
    created_at: datetime
    is_active: bool

# ============ Consent Schemas ============

class ConsentRequest(BaseModel):
    """Schema for user consent submission"""
    data_collection: bool
    data_usage: bool
    analytics: bool

class ConsentResponse(BaseModel):
    """Schema for consent data response"""
    id: str
    user_id: str
    data_collection: bool
    data_usage: bool
    analytics: bool
    consent_timestamp: datetime

# ============ Daily Log Schemas ============

class TransportationEntry(BaseModel):
    """Schema for single transportation entry"""
    mode: str  # car_petrol, car_diesel, bus, train, flight
    distance_km: float = Field(..., ge=0)
    
    @validator('mode')
    def validate_mode(cls, v):
        allowed_modes = ['car_petrol', 'car_diesel', 'bus', 'train', 'flight']
        if v not in allowed_modes:
            raise ValueError(f'Mode must be one of {allowed_modes}')
        return v

class FoodEntry(BaseModel):
    """Schema for single food entry"""
    meal_type: str  # veg, non_veg, vegan
    meals_count: int = Field(..., ge=1)
    
    @validator('meal_type')
    def validate_meal_type(cls, v):
        allowed_types = ['veg', 'non_veg', 'vegan']
        if v not in allowed_types:
            raise ValueError(f'Meal type must be one of {allowed_types}')
        return v

class LifestyleEntry(BaseModel):
    """Schema for single lifestyle entry"""
    category: str  # clothing, electronics
    items_count: int = Field(..., ge=1)
    
    @validator('category')
    def validate_category(cls, v):
        allowed_categories = ['clothing', 'electronics']
        if v not in allowed_categories:
            raise ValueError(f'Category must be one of {allowed_categories}')
        return v

class DailyLogRequest(BaseModel):
    """Schema for daily log submission"""
    date: str  # Format: YYYY-MM-DD
    transportation: Optional[List[TransportationEntry]] = []
    electricity_kwh: Optional[float] = Field(0.0, ge=0)
    food: Optional[List[FoodEntry]] = []
    lifestyle: Optional[List[LifestyleEntry]] = []
    
    @validator('date')
    def validate_date(cls, v):
        try:
            datetime.strptime(v, '%Y-%m-%d')
        except ValueError:
            raise ValueError('Date must be in YYYY-MM-DD format')
        return v

class DailyLogResponse(BaseModel):
    """Schema for daily log response"""
    id: str
    user_id: str
    date: str
    transportation: List[Dict]
    electricity_kwh: float
    food: List[Dict]
    lifestyle: List[Dict]
    transport_emissions: float
    electricity_emissions: float
    food_emissions: float
    lifestyle_emissions: float
    total_emissions: float
    created_at: datetime

# ============ Dashboard Schemas ============

class DashboardSummary(BaseModel):
    """Schema for dashboard summary data"""
    period: str  # 'today', 'weekly', 'monthly'
    total_emissions: float
    transport_emissions: float
    electricity_emissions: float
    food_emissions: float
    lifestyle_emissions: float
    average_daily_emissions: float
    highest_category: str
    comparison_to_average: Optional[float] = None  # % difference from user's average

class DashboardResponse(BaseModel):
    """Schema for complete dashboard response"""
    today: DashboardSummary
    weekly: DashboardSummary
    monthly: DashboardSummary

# ============ History Schemas ============

class HistoryEntry(BaseModel):
    """Schema for single history entry"""
    date: str
    total_emissions: float
    transport_emissions: float
    electricity_emissions: float
    food_emissions: float
    lifestyle_emissions: float

class HistoryResponse(BaseModel):
    """Schema for history response"""
    entries: List[HistoryEntry]
    total_days: int

# ============ Leaderboard Schemas ============

class LeaderboardEntry(BaseModel):
    """Schema for single leaderboard entry"""
    rank: int
    user_name: str
    total_emissions: float
    average_daily_emissions: float

class LeaderboardResponse(BaseModel):
    """Schema for leaderboard response"""
    entries: List[LeaderboardEntry]
    user_rank: Optional[int] = None
    user_emissions: Optional[float] = None

# ============ Recommendations Schemas ============

class Recommendation(BaseModel):
    """Schema for single recommendation"""
    category: str
    title: str
    description: str
    potential_savings_kg: float

class RecommendationsResponse(BaseModel):
    """Schema for recommendations response"""
    recommendations: List[Recommendation]
    highest_emission_category: str
    total_potential_savings: float

# ============ Profile Schemas ============

class ProfileUpdateRequest(BaseModel):
    """Schema for profile update request"""
    name: Optional[str] = None
    age: Optional[int] = Field(None, ge=1, le=150)
    gender: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    # Onboarding preferences
    household_size: Optional[int] = Field(None, ge=1, le=50)
    transport_mode: Optional[str] = None
    diet_type: Optional[str] = None
    energy_source: Optional[str] = None

class ProfileResponse(BaseModel):
    """Schema for profile response"""
    user: UserResponse
    total_logs: int
    total_emissions: float
    average_daily_emissions: float
    member_since: datetime
    has_consent: bool
    onboarding_completed: bool = False  # Whether user has completed onboarding
