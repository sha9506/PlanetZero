"""
Daily Log Routes
Handles daily carbon emission log submission and retrieval
"""
from fastapi import APIRouter, HTTPException, status, Depends
from database import get_database, DAILY_LOGS_COLLECTION
from schemas import DailyLogRequest, DailyLogResponse
from routes.auth import get_current_user
from routes.consent import check_user_consent
from services.emission_service import calculate_total_emissions
from datetime import datetime
from bson import ObjectId

router = APIRouter(prefix="/daily-log", tags=["Daily Log"])

@router.post("", response_model=DailyLogResponse, status_code=status.HTTP_201_CREATED)
async def create_daily_log(
    log_data: DailyLogRequest,
    current_user=Depends(get_current_user)
):
    """
    Submit daily carbon emission log
    
    - Requires user consent
    - Calculates emissions for all categories
    - Stores detailed breakdown
    - Creates/updates carbon footprint entry for charts
    """
    print(f"🔍 Create daily log called")
    print(f"   User: {current_user.get('email') if current_user else 'None'}")
    print(f"   Date: {log_data.date}")
    print(f"   Transportation entries: {len(log_data.transportation)}")
    
    # Check consent
    await check_user_consent(current_user)
    
    db = get_database()
    user_id = str(current_user["_id"])
    user_oid = ObjectId(user_id)
    
    # Check if log already exists for this date
    existing_log = await db[DAILY_LOGS_COLLECTION].find_one({
        "user_id": user_id,
        "date": log_data.date
    })
    
    # Convert Pydantic models to dicts for calculation
    transport_data = [t.dict() for t in log_data.transportation]
    food_data = [f.dict() for f in log_data.food]
    lifestyle_data = [l.dict() for l in log_data.lifestyle]
    
    # Calculate emissions
    emissions_result = calculate_total_emissions(
        transportation_data=transport_data,
        electricity_kwh=log_data.electricity_kwh,
        food_data=food_data,
        lifestyle_data=lifestyle_data
    )
    
    # Create log document
    log_doc = {
        "user_id": user_id,
        "date": log_data.date,
        "transportation": transport_data,
        "electricity_kwh": log_data.electricity_kwh,
        "food": food_data,
        "lifestyle": lifestyle_data,
        "transport_emissions": emissions_result["transport_emissions"],
        "electricity_emissions": emissions_result["electricity_emissions"],
        "food_emissions": emissions_result["food_emissions"],
        "lifestyle_emissions": emissions_result["lifestyle_emissions"],
        "total_emissions": emissions_result["total_emissions"],
        "updated_at": datetime.utcnow()
    }
    
    if existing_log:
        # Update existing log
        log_doc["created_at"] = existing_log["created_at"]
        await db[DAILY_LOGS_COLLECTION].update_one(
            {"_id": existing_log["_id"]},
            {"$set": log_doc}
        )
        log_id = str(existing_log["_id"])
    else:
        # Insert new log
        log_doc["created_at"] = datetime.utcnow()
        result = await db[DAILY_LOGS_COLLECTION].insert_one(log_doc)
        log_id = str(result.inserted_id)
    
    # Parse date string to datetime for carbon_footprints
    log_date = datetime.strptime(log_data.date, '%Y-%m-%d')
    
    # Create/update carbon footprint entry for charts
    footprint_doc = {
        "user_id": user_oid,
        "date": log_date,
        "daily_log_id": ObjectId(log_id),
        "total_emissions": emissions_result["total_emissions"],
        "transport_emissions": emissions_result["transport_emissions"],
        "energy_emissions": emissions_result["electricity_emissions"],
        "food_emissions": emissions_result["food_emissions"],
        "breakdown": {
            "transport": emissions_result["transport_emissions"],
            "electricity": emissions_result["electricity_emissions"],
            "food": emissions_result["food_emissions"],
            "water": 0.0,  # Not tracked yet
            "shopping": emissions_result["lifestyle_emissions"]
        },
        "comparison_to_average": -25.0,  # TODO: Calculate actual comparison
        "created_at": datetime.utcnow()
    }
    
    # Check if footprint exists for this date
    existing_footprint = await db["carbon_footprints"].find_one({
        "user_id": user_oid,
        "date": log_date
    })
    
    if existing_footprint:
        await db["carbon_footprints"].update_one(
            {"_id": existing_footprint["_id"]},
            {"$set": footprint_doc}
        )
    else:
        await db["carbon_footprints"].insert_one(footprint_doc)
    
    return DailyLogResponse(
        id=log_id,
        user_id=user_id,
        date=log_data.date,
        transportation=transport_data,
        electricity_kwh=log_data.electricity_kwh,
        food=food_data,
        lifestyle=lifestyle_data,
        transport_emissions=emissions_result["transport_emissions"],
        electricity_emissions=emissions_result["electricity_emissions"],
        food_emissions=emissions_result["food_emissions"],
        lifestyle_emissions=emissions_result["lifestyle_emissions"],
        total_emissions=emissions_result["total_emissions"],
        created_at=log_doc["created_at"]
    )

@router.get("/{date}", response_model=DailyLogResponse)
async def get_daily_log(date: str, current_user=Depends(get_current_user)):
    """
    Get daily log for a specific date
    
    Args:
        date: Date in YYYY-MM-DD format
    """
    db = get_database()
    user_id = str(current_user["_id"])
    
    # Validate date format
    try:
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid date format. Use YYYY-MM-DD"
        )
    
    log = await db[DAILY_LOGS_COLLECTION].find_one({
        "user_id": user_id,
        "date": date
    })
    
    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No log found for date {date}"
        )
    
    return DailyLogResponse(
        id=str(log["_id"]),
        user_id=user_id,
        date=log["date"],
        transportation=log.get("transportation", []),
        electricity_kwh=log.get("electricity_kwh", 0.0),
        food=log.get("food", []),
        lifestyle=log.get("lifestyle", []),
        transport_emissions=log["transport_emissions"],
        electricity_emissions=log["electricity_emissions"],
        food_emissions=log["food_emissions"],
        lifestyle_emissions=log["lifestyle_emissions"],
        total_emissions=log["total_emissions"],
        created_at=log["created_at"]
    )
