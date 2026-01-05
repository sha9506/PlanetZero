from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

# Enums
class Gender(str, Enum):
    male = "male"
    female = "female"
    other = "other"
    prefer_not_to_say = "prefer_not_to_say"

class TransportMode(str, Enum):
    car_gasoline = "Car (Gasoline)"
    car_diesel = "Car (Diesel)"
    car_electric = "Car (Electric)"
    car_hybrid = "Car (Hybrid)"
    bus = "Bus"
    train = "Train"
    subway = "Subway/Metro"
    bicycle = "Bicycle"
    walking = "Walking"
    motorcycle = "Motorcycle"
    flight = "Flight"

class MealType(str, Enum):
    breakfast = "Breakfast"
    lunch = "Lunch"
    dinner = "Dinner"
    snack = "Snack"

class CommunityCategory(str, Enum):
    general = "general"
    gardening = "gardening"
    recycling = "recycling"
    transport = "transport"
    energy = "energy"
    conservation = "conservation"

class CommunityRole(str, Enum):
    leader = "Community Leader"
    coordinator = "Event Coordinator"
    moderator = "Moderator"
    member = "Member"

class NotificationType(str, Enum):
    achievement = "achievement"
    community = "community"
    recommendation = "recommendation"
    milestone = "milestone"

# User Models
class UserBase(BaseModel):
    email: EmailStr
    name: str
    age: Optional[int] = None
    gender: Optional[Gender] = None
    country: Optional[str] = None
    city: Optional[str] = None
    energy_source: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(UserBase):
    id: str = Field(alias="_id")
    points: int = 0
    total_emissions: float = 0.0
    badges: List[str] = []
    created_at: datetime
    updated_at: datetime
    
    class Config:
        populate_by_name = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Activity Models
class TransportActivity(BaseModel):
    mode: TransportMode
    distance: float
    description: Optional[str] = None

class EnergyUsage(BaseModel):
    electricity: float = 0.0
    heating: float = 0.0

class MealActivity(BaseModel):
    type: MealType
    description: str
    servings: int = 1

class DailyLogCreate(BaseModel):
    date: str
    transport: List[TransportActivity] = []
    energy: EnergyUsage
    meals: List[MealActivity] = []

class DailyLog(DailyLogCreate):
    id: str = Field(alias="_id")
    user_id: str
    carbon_footprint: float
    created_at: datetime
    updated_at: datetime
    
    class Config:
        populate_by_name = True

# Recommendation Models
class RecommendationBase(BaseModel):
    title: str
    description: str
    impact: str  # high, medium, low
    difficulty: str  # easy, medium, hard
    category: str

class Recommendation(RecommendationBase):
    id: str = Field(alias="_id")
    
    class Config:
        populate_by_name = True

class UserRecommendation(BaseModel):
    recommendation_id: str
    completed: bool = False
    completed_at: Optional[datetime] = None

# Community Models
class CommunityBase(BaseModel):
    name: str
    description: str
    category: CommunityCategory
    location: str

class CommunityCreate(CommunityBase):
    pass

class Community(CommunityBase):
    id: str = Field(alias="_id")
    creator_id: str
    members_count: int = 1
    activities: List[str] = []
    created_at: datetime
    updated_at: datetime
    
    class Config:
        populate_by_name = True

class CommunityMember(BaseModel):
    community_id: str
    user_id: str
    role: CommunityRole = CommunityRole.member
    joined_at: datetime

# Badge Models
class BadgeBase(BaseModel):
    name: str
    description: str
    icon: str
    color: str

class Badge(BadgeBase):
    id: str = Field(alias="_id")
    
    class Config:
        populate_by_name = True

class UserBadge(BaseModel):
    user_id: str
    badge_id: str
    earned_at: datetime

# Notification Models
class NotificationCreate(BaseModel):
    user_id: str
    type: NotificationType
    title: str
    message: str

class Notification(NotificationCreate):
    id: str = Field(alias="_id")
    read: bool = False
    created_at: datetime
    
    class Config:
        populate_by_name = True

# Leaderboard Models
class LeaderboardEntry(BaseModel):
    rank: int
    user_id: str
    name: str
    points: int
    emissions: float
    badges: List[str]
    trend: str = "same"  # up, down, same
