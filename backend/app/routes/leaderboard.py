from fastapi import APIRouter, HTTPException, status, Depends
from bson import ObjectId
from typing import List

from app.models import LeaderboardEntry, User
from app.auth import get_current_active_user
from app.database import get_database, USERS_COLLECTION, BADGES_COLLECTION

router = APIRouter()

@router.get("/", response_model=List[LeaderboardEntry])
async def get_leaderboard(
    limit: int = 50,
    current_user: User = Depends(get_current_active_user)
):
    """Get leaderboard rankings"""
    db = get_database()
    
    # Get all users sorted by points
    cursor = db[USERS_COLLECTION].find({}).sort("points", -1).limit(limit)
    users = await cursor.to_list(length=limit)
    
    leaderboard = []
    for idx, user in enumerate(users, 1):
        # Get badge names
        badge_names = []
        if user.get("badges"):
            for badge_id in user["badges"]:
                badge = await db[BADGES_COLLECTION].find_one({"_id": ObjectId(badge_id)})
                if badge:
                    badge_names.append(badge["name"])
        
        # Determine trend (simplified - could be based on historical data)
        trend = "same"
        if idx <= 3:
            trend = "up"
        
        leaderboard.append(LeaderboardEntry(
            rank=idx,
            user_id=str(user["_id"]),
            name=user["name"],
            points=user.get("points", 0),
            emissions=user.get("total_emissions", 0.0),
            badges=badge_names,
            trend=trend
        ))
    
    return leaderboard

@router.get("/user/{user_id}")
async def get_user_rank(
    user_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific user's rank"""
    db = get_database()
    
    # Get user
    user = await db[USERS_COLLECTION].find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Count users with more points
    higher_ranked = await db[USERS_COLLECTION].count_documents({
        "points": {"$gt": user.get("points", 0)}
    })
    
    rank = higher_ranked + 1
    
    # Get badge names
    badge_names = []
    if user.get("badges"):
        for badge_id in user["badges"]:
            badge = await db[BADGES_COLLECTION].find_one({"_id": ObjectId(badge_id)})
            if badge:
                badge_names.append(badge["name"])
    
    return {
        "rank": rank,
        "user_id": user_id,
        "name": user["name"],
        "points": user.get("points", 0),
        "emissions": user.get("total_emissions", 0.0),
        "badges": badge_names
    }

@router.get("/stats")
async def get_leaderboard_stats(current_user: User = Depends(get_current_active_user)):
    """Get overall leaderboard statistics"""
    db = get_database()
    
    total_users = await db[USERS_COLLECTION].count_documents({})
    
    # Get top user
    top_users = await db[USERS_COLLECTION].find({}).sort("points", -1).limit(1).to_list(1)
    top_user_points = top_users[0].get("points", 0) if top_users else 0
    
    # Calculate average points
    pipeline = [
        {"$group": {"_id": None, "avg_points": {"$avg": "$points"}}}
    ]
    result = await db[USERS_COLLECTION].aggregate(pipeline).to_list(1)
    avg_points = result[0]["avg_points"] if result else 0
    
    return {
        "total_users": total_users,
        "top_user_points": top_user_points,
        "average_points": round(avg_points, 2)
    }
