"""
Database Models for MongoDB Collections
These represent the structure of documents stored in MongoDB
"""
from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId

class PyObjectId(ObjectId):
    """Custom ObjectId type for Pydantic"""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

# User Model
class UserModel(BaseModel):
    """User document model"""
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    email: EmailStr
    hashed_password: str
    name: str
    age: Optional[int] = None
    gender: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

# Consent Model
class ConsentModel(BaseModel):
    """User consent document model"""
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    user_id: str
    data_collection: bool
    data_usage: bool
    analytics: bool
    consent_timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

# Daily Log Model
class DailyLogModel(BaseModel):
    """Daily emission log document model"""
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    user_id: str
    date: str  # Format: YYYY-MM-DD
    
    # Transportation data
    transportation: Optional[List[Dict]] = []
    
    # Electricity data
    electricity_kwh: Optional[float] = 0.0
    
    # Food data
    food: Optional[List[Dict]] = []
    
    # Lifestyle data
    lifestyle: Optional[List[Dict]] = []
    
    # Calculated emissions (kg CO₂)
    transport_emissions: float = 0.0
    electricity_emissions: float = 0.0
    food_emissions: float = 0.0
    lifestyle_emissions: float = 0.0
    total_emissions: float = 0.0
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

# Emission Summary Model
class EmissionSummaryModel(BaseModel):
    """Aggregated emission summary document model"""
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    user_id: str
    period: str  # 'daily', 'weekly', 'monthly'
    start_date: str
    end_date: str
    
    total_emissions: float
    transport_emissions: float
    electricity_emissions: float
    food_emissions: float
    lifestyle_emissions: float
    
    average_daily_emissions: float
    highest_category: str
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
