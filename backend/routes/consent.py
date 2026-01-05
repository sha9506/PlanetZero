"""
Consent Routes
Handles user consent submission and retrieval
"""
from fastapi import APIRouter, HTTPException, status, Depends
from database import get_database, CONSENTS_COLLECTION
from schemas import ConsentRequest, ConsentResponse
from routes.auth import get_current_user
from datetime import datetime
from bson import ObjectId

router = APIRouter(prefix="/consent", tags=["Consent"])

@router.post("", response_model=ConsentResponse, status_code=status.HTTP_201_CREATED)
async def submit_consent(consent_data: ConsentRequest, current_user=Depends(get_current_user)):
    """
    Submit user consent for data collection and usage
    
    Required before user can submit any carbon emission data
    """
    db = get_database()
    user_id = str(current_user["_id"])
    
    # Check if consent already exists
    existing_consent = await db[CONSENTS_COLLECTION].find_one({"user_id": user_id})
    
    # Create consent document
    consent_doc = {
        "user_id": user_id,
        "data_collection": consent_data.data_collection,
        "data_usage": consent_data.data_usage,
        "analytics": consent_data.analytics,
        "consent_timestamp": datetime.utcnow()
    }
    
    if existing_consent:
        # Update existing consent
        await db[CONSENTS_COLLECTION].update_one(
            {"user_id": user_id},
            {"$set": consent_doc}
        )
        consent_id = str(existing_consent["_id"])
    else:
        # Insert new consent
        result = await db[CONSENTS_COLLECTION].insert_one(consent_doc)
        consent_id = str(result.inserted_id)
    
    return ConsentResponse(
        id=consent_id,
        user_id=user_id,
        data_collection=consent_data.data_collection,
        data_usage=consent_data.data_usage,
        analytics=consent_data.analytics,
        consent_timestamp=consent_doc["consent_timestamp"]
    )

@router.get("", response_model=ConsentResponse)
async def get_consent(current_user=Depends(get_current_user)):
    """
    Get user's current consent status
    """
    db = get_database()
    user_id = str(current_user["_id"])
    
    consent = await db[CONSENTS_COLLECTION].find_one({"user_id": user_id})
    
    if not consent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consent not found. Please submit consent first."
        )
    
    return ConsentResponse(
        id=str(consent["_id"]),
        user_id=user_id,
        data_collection=consent["data_collection"],
        data_usage=consent["data_usage"],
        analytics=consent["analytics"],
        consent_timestamp=consent["consent_timestamp"]
    )

async def check_user_consent(current_user = Depends(get_current_user)):
    """
    Dependency to check if user has given consent
    
    Used in routes that require consent before data submission
    """
    db = get_database()
    user_id = str(current_user["_id"])
    
    consent = await db[CONSENTS_COLLECTION].find_one({"user_id": user_id})
    
    if not consent:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You must provide consent before submitting data"
        )
    
    if not (consent.get("data_collection") and consent.get("data_usage")):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Data collection and usage consent required"
        )
    
    return True
