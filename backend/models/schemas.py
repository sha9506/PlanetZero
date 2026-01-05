"""
PlanetZero MongoDB Schema Definitions
Pydantic v2 models for all collections with validation
"""
from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional, Dict, Any, List
from datetime import datetime, date
from enum import Enum
from bson import ObjectId


# ============================================================================
# HELPER CLASSES
# ============================================================================

class PyObjectId(ObjectId):
    """Custom ObjectId type for Pydantic v2 compatibility"""
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v, _):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)
    
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type, _handler):
        from pydantic_core import core_schema
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.union_schema([
                core_schema.is_instance_schema(ObjectId),
                core_schema.no_info_plain_validator_function(cls.validate),
            ]),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: str(x)
            ),
        )


# ============================================================================
# ENUMS
# ============================================================================

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"


class DietType(str, Enum):
    VEG = "veg"
    NON_VEG = "non_veg"
    VEGAN = "vegan"


class VehicleType(str, Enum):
    NONE = "none"
    BIKE = "bike"
    CAR = "car"
    ELECTRIC = "electric"


class TransportMode(str, Enum):
    WALK = "walk"
    BIKE = "bike"
    BUS = "bus"
    CAR = "car"
    METRO = "metro"


class FoodCategory(str, Enum):
    VEG = "veg"
    NON_VEG = "non_veg"
    MIXED = "mixed"


class EmissionCategory(str, Enum):
    TRANSPORT = "transport"
    ENERGY = "energy"
    FOOD = "food"


class LeaderboardPeriod(str, Enum):
    WEEKLY = "weekly"
    MONTHLY = "monthly"


# ============================================================================
# COLLECTION 1: USERS
# ============================================================================

class UserModel(BaseModel):
    """
    Core user authentication and identity data.
    Stores credentials, role, and activity tracking.
    """
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr = Field(..., description="Unique email for authentication")
    phone: Optional[str] = Field(None, pattern=r'^\+?[1-9]\d{1,14}$')
    password_hash: str = Field(..., description="Bcrypt hashed password")
    role: UserRole = Field(default=UserRole.USER)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "john@example.com",
                "phone": "+1234567890",
                "password_hash": "$2b$12$KIXXj9Z...",
                "role": "user",
                "is_active": True,
                "created_at": "2026-01-04T10:00:00Z",
                "updated_at": "2026-01-04T10:00:00Z",
                "last_login": None
            }
        }


# ============================================================================
# COLLECTION 2: USER_CONSENTS
# ============================================================================

class UserConsentModel(BaseModel):
    """
    GDPR compliance: tracks user consent acceptance.
    Version tracking allows for consent re-acceptance when terms change.
    """
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    user_id: PyObjectId = Field(..., description="Reference to users collection")
    consent_version: str = Field(..., description="e.g., 'v1.0', 'v2.1'")
    accepted: bool = Field(..., description="Whether user accepted")
    accepted_at: datetime = Field(default_factory=datetime.utcnow)
    ip_address: str = Field(..., description="IP for audit trail")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "user_id": "507f1f77bcf86cd799439011",
                "consent_version": "v1.0",
                "accepted": True,
                "accepted_at": "2026-01-04T10:05:00Z",
                "ip_address": "192.168.1.1",
                "created_at": "2026-01-04T10:05:00Z"
            }
        }


# ============================================================================
# COLLECTION 3: PROFILES
# ============================================================================

class ProfileModel(BaseModel):
    """
    User preferences and personalization data.
    Used for tailoring recommendations and baseline calculations.
    """
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    user_id: PyObjectId = Field(..., description="Reference to users collection")
    age_range: Optional[str] = Field(None, description="e.g., '18-25', '26-35'")
    city: Optional[str] = Field(None, max_length=100)
    country: Optional[str] = Field(None, max_length=100)
    diet_type: Optional[DietType] = None
    household_size: Optional[int] = Field(None, ge=1, le=20)
    vehicle_type: Optional[VehicleType] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "user_id": "507f1f77bcf86cd799439011",
                "age_range": "26-35",
                "city": "Mumbai",
                "country": "India",
                "diet_type": "veg",
                "household_size": 4,
                "vehicle_type": "car",
                "created_at": "2026-01-04T10:00:00Z",
                "updated_at": "2026-01-04T10:00:00Z"
            }
        }


# ============================================================================
# COLLECTION 4: DAILY_LOGS
# ============================================================================

class TransportData(BaseModel):
    """Embedded transport activity data"""
    mode: TransportMode
    distance_km: float = Field(..., ge=0, description="Distance traveled in km")


class DailyLogModel(BaseModel):
    """
    Raw daily activity data entered by users.
    One document per user per day. Used as input for emission calculations.
    """
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    user_id: PyObjectId = Field(..., description="Reference to users collection")
    date: date = Field(..., description="Date of activity (YYYY-MM-DD)")
    transport: Optional[TransportData] = None
    electricity_units: Optional[float] = Field(None, ge=0, description="kWh consumed")
    water_liters: Optional[float] = Field(None, ge=0, description="Liters of water used")
    food_category: Optional[FoodCategory] = None
    shopping_spend: Optional[float] = Field(None, ge=0, description="Spending in local currency")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "user_id": "507f1f77bcf86cd799439011",
                "date": "2026-01-04",
                "transport": {
                    "mode": "car",
                    "distance_km": 25.5
                },
                "electricity_units": 12.3,
                "water_liters": 150.0,
                "food_category": "veg",
                "shopping_spend": 500.0,
                "created_at": "2026-01-04T20:00:00Z"
            }
        }


# ============================================================================
# COLLECTION 5: EMISSION_FACTORS
# ============================================================================

class EmissionFactorModel(BaseModel):
    """
    Static reference data for emission calculations.
    Region-specific factors allow for localized accuracy.
    Source tracking ensures credibility and auditability.
    """
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    category: EmissionCategory
    type: str = Field(..., description="e.g., 'petrol_car', 'coal_electricity'")
    unit: str = Field(..., description="e.g., 'km', 'kWh', 'kg'")
    co2e_per_unit: float = Field(..., ge=0, description="CO2 equivalent per unit")
    region: str = Field(..., description="e.g., 'India', 'Global', 'Europe'")
    source: str = Field(..., description="Data source reference")
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "category": "transport",
                "type": "petrol_car",
                "unit": "km",
                "co2e_per_unit": 0.192,
                "region": "India",
                "source": "IPCC 2023 Guidelines",
                "updated_at": "2026-01-01T00:00:00Z"
            }
        }


# ============================================================================
# COLLECTION 6: CARBON_FOOTPRINTS
# ============================================================================

class CarbonFootprintModel(BaseModel):
    """
    Computed carbon emission results.
    One document per user per day after calculation.
    Comparison to average helps users understand their impact.
    """
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    user_id: PyObjectId = Field(..., description="Reference to users collection")
    date: date = Field(..., description="Date of calculation")
    total_emissions: float = Field(..., ge=0, description="Total CO2e in kg")
    transport_emissions: float = Field(default=0.0, ge=0)
    energy_emissions: float = Field(default=0.0, ge=0)
    food_emissions: float = Field(default=0.0, ge=0)
    comparison_to_average: float = Field(
        ..., 
        description="% difference from regional average (positive = above avg)"
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "user_id": "507f1f77bcf86cd799439011",
                "date": "2026-01-04",
                "total_emissions": 15.8,
                "transport_emissions": 4.9,
                "energy_emissions": 10.1,
                "food_emissions": 0.8,
                "comparison_to_average": -12.5,
                "created_at": "2026-01-04T21:00:00Z"
            }
        }


# ============================================================================
# COLLECTION 7: RECOMMENDATIONS
# ============================================================================

class RecommendationModel(BaseModel):
    """
    AI or rule-based sustainability suggestions.
    Impact score helps prioritize high-value changes.
    is_applied tracks user adoption for effectiveness measurement.
    """
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    user_id: PyObjectId = Field(..., description="Reference to users collection")
    category: str = Field(..., description="e.g., 'transport', 'energy', 'food'")
    message: str = Field(..., max_length=500)
    impact_score: int = Field(..., ge=1, le=10, description="1=low, 10=high impact")
    is_applied: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "user_id": "507f1f77bcf86cd799439011",
                "category": "transport",
                "message": "Switch to metro for your daily commute to reduce emissions by 60%",
                "impact_score": 8,
                "is_applied": False,
                "created_at": "2026-01-04T10:00:00Z"
            }
        }


# ============================================================================
# COLLECTION 8: LEADERBOARD
# ============================================================================

class LeaderboardModel(BaseModel):
    """
    Cached leaderboard scores for performance.
    Calculated periodically via batch job.
    Lower score = better (less emissions).
    """
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    period: LeaderboardPeriod
    user_id: PyObjectId = Field(..., description="Reference to users collection")
    score: float = Field(..., ge=0, description="Total emissions for period in kg CO2e")
    rank: int = Field(..., ge=1, description="Position in leaderboard")
    calculated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "period": "weekly",
                "user_id": "507f1f77bcf86cd799439011",
                "score": 85.3,
                "rank": 42,
                "calculated_at": "2026-01-04T00:00:00Z"
            }
        }


# ============================================================================
# COLLECTION 9: COMMUNITY_POSTS
# ============================================================================

class CommunityPostModel(BaseModel):
    """
    Community feed posts for user engagement.
    Denormalized counts (likes, comments) for performance.
    """
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    user_id: PyObjectId = Field(..., description="Reference to users collection")
    content: str = Field(..., min_length=1, max_length=2000)
    likes_count: int = Field(default=0, ge=0)
    comments_count: int = Field(default=0, ge=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "user_id": "507f1f77bcf86cd799439011",
                "content": "Just completed my first week of cycling to work! Feeling great and helping the planet 🌍🚴‍♂️",
                "likes_count": 23,
                "comments_count": 5,
                "created_at": "2026-01-04T09:00:00Z",
                "updated_at": "2026-01-04T09:00:00Z"
            }
        }


# ============================================================================
# COLLECTION 10: COMMUNITY_COMMENTS
# ============================================================================

class CommunityCommentModel(BaseModel):
    """
    Comments on community posts.
    Separate collection for scalability (posts with 100s of comments).
    """
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    post_id: PyObjectId = Field(..., description="Reference to community_posts")
    user_id: PyObjectId = Field(..., description="Reference to users collection")
    comment: str = Field(..., min_length=1, max_length=500)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "post_id": "507f1f77bcf86cd799439012",
                "user_id": "507f1f77bcf86cd799439011",
                "comment": "That's awesome! How many km is your commute?",
                "created_at": "2026-01-04T10:00:00Z"
            }
        }


# ============================================================================
# COLLECTION 11: ACTIVITY_HISTORY
# ============================================================================

class ActivityHistoryModel(BaseModel):
    """
    Audit trail for important user actions.
    Metadata field stores flexible action-specific data.
    Useful for debugging, analytics, and compliance.
    """
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    user_id: PyObjectId = Field(..., description="Reference to users collection")
    action: str = Field(..., description="e.g., 'login', 'update_profile', 'submit_log'")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Action-specific data")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "user_id": "507f1f77bcf86cd799439011",
                "action": "submit_daily_log",
                "metadata": {
                    "date": "2026-01-04",
                    "categories": ["transport", "energy"]
                },
                "timestamp": "2026-01-04T20:00:00Z"
            }
        }


# ============================================================================
# COLLECTION 12: NOTIFICATIONS
# ============================================================================

class NotificationModel(BaseModel):
    """
    In-app notifications for user engagement.
    Type field allows for different notification categories/styles.
    is_read enables unread badge counts.
    """
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    user_id: PyObjectId = Field(..., description="Reference to users collection")
    type: str = Field(..., description="e.g., 'achievement', 'reminder', 'social'")
    message: str = Field(..., max_length=200)
    is_read: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "user_id": "507f1f77bcf86cd799439011",
                "type": "achievement",
                "message": "Congratulations! You've reduced your carbon footprint by 20% this week!",
                "is_read": False,
                "created_at": "2026-01-04T18:00:00Z"
            }
        }
