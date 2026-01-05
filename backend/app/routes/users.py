from fastapi import APIRouter, HTTPException, status, Depends
from bson import ObjectId
from datetime import datetime

from app.models import User, UserBase
from app.auth import get_current_active_user
from app.database import get_database, USERS_COLLECTION

router = APIRouter()

@router.get("/me", response_model=User)
async def get_current_user_profile(current_user: User = Depends(get_current_active_user)):
    """Get current user profile"""
    return current_user

@router.put("/me", response_model=User)
async def update_user_profile(
    user_update: UserBase,
    current_user: User = Depends(get_current_active_user)
):
    """Update current user profile"""
    db = get_database()
    
    update_data = user_update.model_dump(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()
    
    result = await db[USERS_COLLECTION].update_one(
        {"_id": ObjectId(current_user.id)},
        {"$set": update_data}
    )
    
    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Retrieve updated user
    updated_user = await db[USERS_COLLECTION].find_one({"_id": ObjectId(current_user.id)})
    updated_user["_id"] = str(updated_user["_id"])
    
    return User(**updated_user)

@router.post("/onboarding")
async def complete_onboarding(
    onboarding_data: dict,
    current_user: User = Depends(get_current_active_user)
):
    """Complete user onboarding"""
    db = get_database()
    
    update_data = {
        **onboarding_data,
        "onboarding_completed": True,
        "onboarding_date": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    result = await db[USERS_COLLECTION].update_one(
        {"_id": ObjectId(current_user.id)},
        {"$set": update_data}
    )
    
    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {"message": "Onboarding completed successfully"}

@router.get("/{user_id}", response_model=User)
async def get_user_by_id(
    user_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get user by ID"""
    db = get_database()
    
    user = await db[USERS_COLLECTION].find_one({"_id": ObjectId(user_id)})
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user["_id"] = str(user["_id"])
    return User(**user)
