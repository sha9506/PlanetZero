from fastapi import APIRouter, HTTPException, status, Depends
from bson import ObjectId
from datetime import datetime
from typing import List

from app.models import DailyLogCreate, DailyLog, User
from app.auth import get_current_active_user
from app.database import get_database, DAILY_LOGS_COLLECTION, USERS_COLLECTION, NOTIFICATIONS_COLLECTION

router = APIRouter()

# Emission factors (kg CO2 per unit)
EMISSION_FACTORS = {
    "Car (Gasoline)": 0.21,  # per km
    "Car (Diesel)": 0.17,
    "Car (Electric)": 0.05,
    "Car (Hybrid)": 0.12,
    "Bus": 0.08,
    "Train": 0.04,
    "Subway/Metro": 0.03,
    "Bicycle": 0.0,
    "Walking": 0.0,
    "Motorcycle": 0.15,
    "Flight": 0.25,
}

ENERGY_FACTOR = 0.5  # kg CO2 per kWh
MEAL_FACTOR = 2.0  # kg CO2 per serving (average)

def calculate_carbon_footprint(daily_log: DailyLogCreate) -> float:
    """Calculate total carbon footprint for a daily log"""
    total = 0.0
    
    # Transport emissions
    for transport in daily_log.transport:
        factor = EMISSION_FACTORS.get(transport.mode, 0.0)
        total += factor * transport.distance
    
    # Energy emissions
    total += (daily_log.energy.electricity + daily_log.energy.heating) * ENERGY_FACTOR
    
    # Meal emissions
    total += len(daily_log.meals) * MEAL_FACTOR
    
    return round(total, 2)

@router.post("/daily-logs", response_model=DailyLog, status_code=status.HTTP_201_CREATED)
async def create_daily_log(
    daily_log: DailyLogCreate,
    current_user: User = Depends(get_current_active_user)
):
    """Create a new daily log entry"""
    db = get_database()
    
    # Check if log already exists for this date
    existing_log = await db[DAILY_LOGS_COLLECTION].find_one({
        "user_id": current_user.id,
        "date": daily_log.date
    })
    
    if existing_log:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Daily log already exists for {daily_log.date}"
        )
    
    # Calculate carbon footprint
    carbon_footprint = calculate_carbon_footprint(daily_log)
    
    # Create log document
    log_dict = daily_log.model_dump()
    log_dict.update({
        "user_id": current_user.id,
        "carbon_footprint": carbon_footprint,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    })
    
    # Insert log
    result = await db[DAILY_LOGS_COLLECTION].insert_one(log_dict)
    
    # Update user's total emissions
    await db[USERS_COLLECTION].update_one(
        {"_id": ObjectId(current_user.id)},
        {
            "$inc": {"total_emissions": carbon_footprint, "points": 10},
            "$set": {"updated_at": datetime.utcnow()}
        }
    )
    
    # Create notification for logging
    await db[NOTIFICATIONS_COLLECTION].insert_one({
        "user_id": current_user.id,
        "type": "milestone",
        "title": "Daily Log Saved!",
        "message": f"Your carbon footprint for today: {carbon_footprint} kg CO2",
        "read": False,
        "created_at": datetime.utcnow()
    })
    
    # Retrieve created log
    created_log = await db[DAILY_LOGS_COLLECTION].find_one({"_id": result.inserted_id})
    created_log["_id"] = str(created_log["_id"])
    
    return DailyLog(**created_log)

@router.get("/daily-logs", response_model=List[DailyLog])
async def get_daily_logs(
    current_user: User = Depends(get_current_active_user),
    limit: int = 30
):
    """Get user's daily logs"""
    db = get_database()
    
    cursor = db[DAILY_LOGS_COLLECTION].find(
        {"user_id": current_user.id}
    ).sort("date", -1).limit(limit)
    
    logs = await cursor.to_list(length=limit)
    
    for log in logs:
        log["_id"] = str(log["_id"])
    
    return [DailyLog(**log) for log in logs]

@router.get("/daily-logs/{log_id}", response_model=DailyLog)
async def get_daily_log(
    log_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific daily log"""
    db = get_database()
    
    log = await db[DAILY_LOGS_COLLECTION].find_one({
        "_id": ObjectId(log_id),
        "user_id": current_user.id
    })
    
    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Daily log not found"
        )
    
    log["_id"] = str(log["_id"])
    return DailyLog(**log)

@router.put("/daily-logs/{log_id}", response_model=DailyLog)
async def update_daily_log(
    log_id: str,
    daily_log_update: DailyLogCreate,
    current_user: User = Depends(get_current_active_user)
):
    """Update a daily log"""
    db = get_database()
    
    # Get existing log
    existing_log = await db[DAILY_LOGS_COLLECTION].find_one({
        "_id": ObjectId(log_id),
        "user_id": current_user.id
    })
    
    if not existing_log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Daily log not found"
        )
    
    # Calculate new carbon footprint
    new_carbon = calculate_carbon_footprint(daily_log_update)
    old_carbon = existing_log["carbon_footprint"]
    carbon_diff = new_carbon - old_carbon
    
    # Update log
    update_dict = daily_log_update.model_dump()
    update_dict.update({
        "carbon_footprint": new_carbon,
        "updated_at": datetime.utcnow()
    })
    
    await db[DAILY_LOGS_COLLECTION].update_one(
        {"_id": ObjectId(log_id)},
        {"$set": update_dict}
    )
    
    # Update user's total emissions
    await db[USERS_COLLECTION].update_one(
        {"_id": ObjectId(current_user.id)},
        {
            "$inc": {"total_emissions": carbon_diff},
            "$set": {"updated_at": datetime.utcnow()}
        }
    )
    
    # Retrieve updated log
    updated_log = await db[DAILY_LOGS_COLLECTION].find_one({"_id": ObjectId(log_id)})
    updated_log["_id"] = str(updated_log["_id"])
    
    return DailyLog(**updated_log)

@router.delete("/daily-logs/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_daily_log(
    log_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Delete a daily log"""
    db = get_database()
    
    # Get existing log
    existing_log = await db[DAILY_LOGS_COLLECTION].find_one({
        "_id": ObjectId(log_id),
        "user_id": current_user.id
    })
    
    if not existing_log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Daily log not found"
        )
    
    # Delete log
    await db[DAILY_LOGS_COLLECTION].delete_one({"_id": ObjectId(log_id)})
    
    # Update user's total emissions
    await db[USERS_COLLECTION].update_one(
        {"_id": ObjectId(current_user.id)},
        {
            "$inc": {"total_emissions": -existing_log["carbon_footprint"]},
            "$set": {"updated_at": datetime.utcnow()}
        }
    )
    
    return None

@router.get("/stats")
async def get_activity_stats(current_user: User = Depends(get_current_active_user)):
    """Get user's activity statistics"""
    db = get_database()
    
    # Get all logs
    logs = await db[DAILY_LOGS_COLLECTION].find(
        {"user_id": current_user.id}
    ).to_list(length=None)
    
    if not logs:
        return {
            "total_logs": 0,
            "total_emissions": 0.0,
            "average_daily_emissions": 0.0,
            "total_transport_activities": 0,
            "total_meals_logged": 0
        }
    
    total_emissions = sum(log["carbon_footprint"] for log in logs)
    total_transport = sum(len(log["transport"]) for log in logs)
    total_meals = sum(len(log["meals"]) for log in logs)
    
    return {
        "total_logs": len(logs),
        "total_emissions": round(total_emissions, 2),
        "average_daily_emissions": round(total_emissions / len(logs), 2),
        "total_transport_activities": total_transport,
        "total_meals_logged": total_meals
    }
