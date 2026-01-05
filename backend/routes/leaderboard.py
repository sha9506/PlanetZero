"""
Leaderboard Routes
Provides ranking of users based on lowest carbon emissions
"""
from fastapi import APIRouter, HTTPException, status, Depends, Query
from database import get_database, DAILY_LOGS_COLLECTION, USERS_COLLECTION
from schemas import LeaderboardEntry, LeaderboardResponse
from routes.auth import get_current_user
from datetime import datetime, timedelta

router = APIRouter(prefix="/leaderboard", tags=["Leaderboard"])

@router.get("", response_model=LeaderboardResponse)
async def get_leaderboard(
    current_user=Depends(get_current_user),
    period: str = Query("monthly", regex="^(weekly|monthly|all_time)$"),
    limit: int = Query(10, ge=5, le=100)
):
    """
    Get leaderboard of users with lowest emissions
    
    Args:
        period: Time period for leaderboard (weekly, monthly, all_time)
        limit: Number of top users to return (default: 10)
    
    Returns:
        Leaderboard with top users ranked by lowest average daily emissions
    """
    db = get_database()
    current_user_id = str(current_user["_id"])
    
    # Calculate date range based on period
    today = datetime.utcnow().date()
    
    if period == "weekly":
        start_date = (today - timedelta(days=6)).strftime('%Y-%m-%d')
    elif period == "monthly":
        start_date = (today - timedelta(days=29)).strftime('%Y-%m-%d')
    else:  # all_time
        start_date = None
    
    # Build aggregation pipeline
    pipeline = []
    
    # Match logs for the period
    if start_date:
        pipeline.append({
            "$match": {
                "date": {"$gte": start_date}
            }
        })
    
    # Group by user and calculate total emissions
    pipeline.extend([
        {
            "$group": {
                "_id": "$user_id",
                "total_emissions": {"$sum": "$total_emissions"},
                "log_count": {"$sum": 1}
            }
        },
        {
            "$project": {
                "user_id": "$_id",
                "total_emissions": 1,
                "log_count": 1,
                "average_daily_emissions": {
                    "$divide": ["$total_emissions", "$log_count"]
                }
            }
        },
        # Sort by average daily emissions (lowest first)
        {
            "$sort": {"average_daily_emissions": 1}
        },
        {
            "$limit": limit
        }
    ])
    
    # Execute aggregation
    results = await db[DAILY_LOGS_COLLECTION].aggregate(pipeline).to_list(length=limit)
    
    # Fetch user names
    user_ids = [result["user_id"] for result in results]
    from bson import ObjectId
    users = await db[USERS_COLLECTION].find({
        "_id": {"$in": [ObjectId(uid) for uid in user_ids]}
    }).to_list(length=len(user_ids))
    
    # Create user name mapping
    user_names = {str(user["_id"]): user["name"] for user in users}
    
    # Build leaderboard entries
    entries = []
    user_rank = None
    user_emissions = None
    
    for idx, result in enumerate(results, start=1):
        user_id = result["user_id"]
        entry = LeaderboardEntry(
            rank=idx,
            user_name=user_names.get(user_id, "Unknown User"),
            total_emissions=round(result["total_emissions"], 3),
            average_daily_emissions=round(result["average_daily_emissions"], 3)
        )
        entries.append(entry)
        
        # Track current user's rank
        if user_id == current_user_id:
            user_rank = idx
            user_emissions = round(result["average_daily_emissions"], 3)
    
    # If current user is not in top results, find their rank
    if user_rank is None:
        # Count users with lower emissions than current user
        current_user_pipeline = [
            {
                "$match": {
                    "user_id": current_user_id
                }
            }
        ]
        
        if start_date:
            current_user_pipeline[0]["$match"]["date"] = {"$gte": start_date}
        
        current_user_pipeline.extend([
            {
                "$group": {
                    "_id": "$user_id",
                    "total_emissions": {"$sum": "$total_emissions"},
                    "log_count": {"$sum": 1}
                }
            },
            {
                "$project": {
                    "average_daily_emissions": {
                        "$divide": ["$total_emissions", "$log_count"]
                    }
                }
            }
        ])
        
        current_user_result = await db[DAILY_LOGS_COLLECTION].aggregate(
            current_user_pipeline
        ).to_list(length=1)
        
        if current_user_result:
            user_emissions = round(current_user_result[0]["average_daily_emissions"], 3)
            
            # Count how many users have lower emissions
            count_pipeline = pipeline[:-1]  # Remove limit
            count_pipeline.append({
                "$match": {
                    "average_daily_emissions": {"$lt": user_emissions}
                }
            })
            count_pipeline.append({"$count": "count"})
            
            count_result = await db[DAILY_LOGS_COLLECTION].aggregate(
                count_pipeline
            ).to_list(length=1)
            
            user_rank = count_result[0]["count"] + 1 if count_result else 1
    
    return LeaderboardResponse(
        entries=entries,
        user_rank=user_rank,
        user_emissions=user_emissions
    )
