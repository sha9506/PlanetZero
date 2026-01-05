from fastapi import APIRouter, HTTPException, status, Depends
from bson import ObjectId
from typing import List
from datetime import datetime

from app.models import Recommendation, User
from app.auth import get_current_active_user
from app.database import get_database, RECOMMENDATIONS_COLLECTION, USERS_COLLECTION, NOTIFICATIONS_COLLECTION

router = APIRouter()

# Initialize recommendations data
INITIAL_RECOMMENDATIONS = [
    {
        "title": "Switch to LED Bulbs",
        "description": "Replace traditional bulbs with energy-efficient LED lights to reduce electricity consumption by up to 75%.",
        "impact": "high",
        "difficulty": "easy",
        "category": "energy"
    },
    {
        "title": "Start Composting",
        "description": "Turn your food waste into nutrient-rich compost for your garden, reducing landfill waste.",
        "impact": "medium",
        "difficulty": "medium",
        "category": "lifestyle"
    },
    {
        "title": "Use Public Transport",
        "description": "Take the bus or train instead of driving alone to significantly reduce your carbon emissions.",
        "impact": "high",
        "difficulty": "medium",
        "category": "transport"
    },
    {
        "title": "Reduce Meat Consumption",
        "description": "Try Meatless Mondays or reduce meat portions to lower your carbon footprint from food production.",
        "impact": "high",
        "difficulty": "medium",
        "category": "food"
    },
    {
        "title": "Install Smart Thermostat",
        "description": "Optimize your home heating and cooling automatically, saving energy and money.",
        "impact": "high",
        "difficulty": "hard",
        "category": "energy"
    },
    {
        "title": "Buy Local Produce",
        "description": "Support local farmers and reduce transportation emissions by buying seasonal, local food.",
        "impact": "medium",
        "difficulty": "easy",
        "category": "food"
    },
    {
        "title": "Bike to Work",
        "description": "Cycle instead of driving for short commutes. It's healthy and emission-free!",
        "impact": "high",
        "difficulty": "medium",
        "category": "transport"
    },
    {
        "title": "Reduce Water Usage",
        "description": "Take shorter showers and fix leaky faucets to conserve water and reduce energy for water heating.",
        "impact": "medium",
        "difficulty": "easy",
        "category": "lifestyle"
    },
    {
        "title": "Switch to Renewable Energy",
        "description": "Choose a green energy provider or install solar panels to power your home sustainably.",
        "impact": "high",
        "difficulty": "hard",
        "category": "energy"
    },
    {
        "title": "Use Reusable Bags",
        "description": "Eliminate single-use plastic bags by bringing your own reusable shopping bags.",
        "impact": "low",
        "difficulty": "easy",
        "category": "lifestyle"
    }
]

@router.get("/", response_model=List[Recommendation])
async def get_recommendations(current_user: User = Depends(get_current_active_user)):
    """Get all recommendations"""
    db = get_database()
    
    # Check if recommendations exist, if not initialize them
    count = await db[RECOMMENDATIONS_COLLECTION].count_documents({})
    if count == 0:
        await db[RECOMMENDATIONS_COLLECTION].insert_many(INITIAL_RECOMMENDATIONS)
    
    cursor = db[RECOMMENDATIONS_COLLECTION].find({})
    recommendations = await cursor.to_list(length=None)
    
    for rec in recommendations:
        rec["_id"] = str(rec["_id"])
    
    return [Recommendation(**rec) for rec in recommendations]

@router.get("/{recommendation_id}", response_model=Recommendation)
async def get_recommendation(
    recommendation_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific recommendation"""
    db = get_database()
    
    rec = await db[RECOMMENDATIONS_COLLECTION].find_one({"_id": ObjectId(recommendation_id)})
    
    if not rec:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recommendation not found"
        )
    
    rec["_id"] = str(rec["_id"])
    return Recommendation(**rec)

@router.post("/{recommendation_id}/complete")
async def mark_recommendation_complete(
    recommendation_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Mark a recommendation as completed"""
    db = get_database()
    
    # Verify recommendation exists
    rec = await db[RECOMMENDATIONS_COLLECTION].find_one({"_id": ObjectId(recommendation_id)})
    if not rec:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recommendation not found"
        )
    
    # Update user's completed recommendations
    user = await db[USERS_COLLECTION].find_one({"_id": ObjectId(current_user.id)})
    completed_recs = user.get("completed_recommendations", [])
    
    if recommendation_id in completed_recs:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Recommendation already completed"
        )
    
    # Add to completed list and award points
    points_awarded = 50
    await db[USERS_COLLECTION].update_one(
        {"_id": ObjectId(current_user.id)},
        {
            "$push": {"completed_recommendations": recommendation_id},
            "$inc": {"points": points_awarded},
            "$set": {"updated_at": datetime.utcnow()}
        }
    )
    
    # Create achievement notification
    await db[NOTIFICATIONS_COLLECTION].insert_one({
        "user_id": current_user.id,
        "type": "achievement",
        "title": "Recommendation Completed!",
        "message": f"You earned {points_awarded} points for completing: {rec['title']}",
        "read": False,
        "created_at": datetime.utcnow()
    })
    
    return {
        "message": "Recommendation marked as completed",
        "points_awarded": points_awarded
    }

@router.post("/{recommendation_id}/uncomplete")
async def mark_recommendation_incomplete(
    recommendation_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Mark a recommendation as not completed"""
    db = get_database()
    
    # Remove from completed list
    result = await db[USERS_COLLECTION].update_one(
        {"_id": ObjectId(current_user.id)},
        {
            "$pull": {"completed_recommendations": recommendation_id},
            "$inc": {"points": -50},
            "$set": {"updated_at": datetime.utcnow()}
        }
    )
    
    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Recommendation was not marked as completed"
        )
    
    return {"message": "Recommendation marked as not completed"}

@router.get("/user/completed")
async def get_user_completed_recommendations(
    current_user: User = Depends(get_current_active_user)
):
    """Get user's completed recommendations"""
    db = get_database()
    
    user = await db[USERS_COLLECTION].find_one({"_id": ObjectId(current_user.id)})
    completed_ids = user.get("completed_recommendations", [])
    
    if not completed_ids:
        return []
    
    # Convert string IDs to ObjectIds
    object_ids = [ObjectId(id) for id in completed_ids if ObjectId.is_valid(id)]
    
    cursor = db[RECOMMENDATIONS_COLLECTION].find({"_id": {"$in": object_ids}})
    recommendations = await cursor.to_list(length=None)
    
    for rec in recommendations:
        rec["_id"] = str(rec["_id"])
    
    return [Recommendation(**rec) for rec in recommendations]
