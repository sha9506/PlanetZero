"""
Profile Routes
Handles user profile retrieval and updates
"""
from fastapi import APIRouter, HTTPException, status, Depends
from database import get_database, USERS_COLLECTION, DAILY_LOGS_COLLECTION, CONSENTS_COLLECTION
from schemas import ProfileResponse, ProfileUpdateRequest, UserResponse
from routes.auth import get_current_user
from datetime import datetime
from bson import ObjectId

router = APIRouter(prefix="/profile", tags=["Profile"])

@router.get("", response_model=ProfileResponse)
async def get_profile(current_user=Depends(get_current_user)):
    """
    Get user profile with emission statistics
    
    Returns:
        - User details
        - Total logs count
        - Total emissions
        - Average daily emissions
        - Consent status
    """
    db = get_database()
    user_id = str(current_user["_id"])
    
    # Get user's logs
    logs = await db[DAILY_LOGS_COLLECTION].find({"user_id": user_id}).to_list(length=1000)
    
    # Calculate statistics
    total_logs = len(logs)
    total_emissions = sum(log.get("total_emissions", 0) for log in logs)
    average_daily_emissions = total_emissions / total_logs if total_logs > 0 else 0.0
    
    # Check consent status
    consent = await db[CONSENTS_COLLECTION].find_one({"user_id": user_id})
    has_consent = consent is not None
    
    # Check if onboarding is completed (has country and city at minimum)
    onboarding_completed = bool(
        current_user.get("country") and 
        current_user.get("city")
    )
    
    # Build user response
    user_response = UserResponse(
        id=user_id,
        email=current_user["email"],
        name=current_user["name"],
        age=current_user.get("age"),
        gender=current_user.get("gender"),
        country=current_user.get("country"),
        city=current_user.get("city"),
        created_at=current_user["created_at"],
        is_active=current_user.get("is_active", True)
    )
    
    return ProfileResponse(
        user=user_response,
        total_logs=total_logs,
        total_emissions=round(total_emissions, 3),
        average_daily_emissions=round(average_daily_emissions, 3),
        member_since=current_user["created_at"],
        has_consent=has_consent,
        onboarding_completed=onboarding_completed
    )

@router.put("", response_model=UserResponse)
async def update_profile(
    profile_data: ProfileUpdateRequest,
    current_user=Depends(get_current_user)
):
    """
    Update user profile information
    
    Allows updating:
        - Name
        - Age
        - Gender
        - Country
        - City
        - Onboarding preferences (household_size, transport_mode, diet_type, energy_source)
    """
    db = get_database()
    user_id = current_user["_id"]
    
    # Build update document (only include provided fields)
    update_doc = {"updated_at": datetime.utcnow()}
    
    if profile_data.name is not None:
        update_doc["name"] = profile_data.name
    if profile_data.age is not None:
        update_doc["age"] = profile_data.age
    if profile_data.gender is not None:
        update_doc["gender"] = profile_data.gender
    if profile_data.country is not None:
        update_doc["country"] = profile_data.country
    if profile_data.city is not None:
        update_doc["city"] = profile_data.city
    # Onboarding preferences
    if profile_data.household_size is not None:
        update_doc["household_size"] = profile_data.household_size
    if profile_data.transport_mode is not None:
        update_doc["transport_mode"] = profile_data.transport_mode
    if profile_data.diet_type is not None:
        update_doc["diet_type"] = profile_data.diet_type
    if profile_data.energy_source is not None:
        update_doc["energy_source"] = profile_data.energy_source
    
    # Update user document
    await db[USERS_COLLECTION].update_one(
        {"_id": user_id},
        {"$set": update_doc}
    )
    
    # Fetch updated user
    updated_user = await db[USERS_COLLECTION].find_one({"_id": user_id})
    
    return UserResponse(
        id=str(updated_user["_id"]),
        email=updated_user["email"],
        name=updated_user["name"],
        age=updated_user.get("age"),
        gender=updated_user.get("gender"),
        country=updated_user.get("country"),
        city=updated_user.get("city"),
        created_at=updated_user["created_at"],
        is_active=updated_user.get("is_active", True)
    )
