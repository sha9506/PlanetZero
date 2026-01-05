"""
History Routes
Provides date-wise emission history for the user
"""
from fastapi import APIRouter, HTTPException, status, Depends, Query
from database import get_database, DAILY_LOGS_COLLECTION
from schemas import HistoryEntry, HistoryResponse
from routes.auth import get_current_user
from typing import Optional
from datetime import datetime, timedelta

router = APIRouter(prefix="/history", tags=["History"])

@router.get("", response_model=HistoryResponse)
async def get_history(
    current_user=Depends(get_current_user),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    limit: int = Query(30, ge=1, le=365, description="Number of days to fetch")
):
    """
    Get emission history for the user
    
    Args:
        start_date: Optional start date filter
        end_date: Optional end date filter
        limit: Maximum number of records to return (default: 30)
    
    Returns:
        List of daily emission records sorted by date (newest first)
    """
    db = get_database()
    user_id = str(current_user["_id"])
    
    # Build query
    query = {"user_id": user_id}
    
    # Add date filters if provided
    if start_date or end_date:
        date_filter = {}
        
        if start_date:
            try:
                datetime.strptime(start_date, '%Y-%m-%d')
                date_filter["$gte"] = start_date
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid start_date format. Use YYYY-MM-DD"
                )
        
        if end_date:
            try:
                datetime.strptime(end_date, '%Y-%m-%d')
                date_filter["$lte"] = end_date
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid end_date format. Use YYYY-MM-DD"
                )
        
        query["date"] = date_filter
    
    # Fetch logs from database
    logs = await db[DAILY_LOGS_COLLECTION].find(query).sort("date", -1).limit(limit).to_list(length=limit)
    
    # Convert to history entries
    entries = []
    for log in logs:
        entries.append(HistoryEntry(
            date=log["date"],
            total_emissions=log.get("total_emissions", 0.0),
            transport_emissions=log.get("transport_emissions", 0.0),
            electricity_emissions=log.get("electricity_emissions", 0.0),
            food_emissions=log.get("food_emissions", 0.0),
            lifestyle_emissions=log.get("lifestyle_emissions", 0.0)
        ))
    
    return HistoryResponse(
        entries=entries,
        total_days=len(entries)
    )
