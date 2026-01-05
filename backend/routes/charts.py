"""
Charts Routes
Provides chart data for dashboard visualizations
"""
from fastapi import APIRouter, HTTPException, status, Depends
from database import get_database
from routes.auth import get_current_user
from services.chart_service import ChartService
from datetime import datetime, timedelta
from typing import Dict, Any
from pydantic import BaseModel
from bson import ObjectId

router = APIRouter(prefix="/charts", tags=["Charts"])


class ChartsResponse(BaseModel):
    """Response model for charts data"""
    monthly_trend: Dict[str, Any]
    category_breakdown: Dict[str, Any]
    weekly_comparison: Dict[str, Any]


@router.get("", response_model=ChartsResponse)
async def get_charts(
    days: int = 30,
    current_user=Depends(get_current_user)
):
    """
    Get chart data for dashboard visualizations
    
    Args:
        days: Number of days to include in charts (default: 30)
        current_user: Authenticated user from token
    
    Returns:
        Chart data for monthly trend, category breakdown, and weekly comparison
    """
    db = get_database()
    user_id = ObjectId(str(current_user["_id"]))
    
    print(f"🔍 Fetching charts for user: {user_id}")
    
    # Calculate date range
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days - 1)
    
    print(f"   Date range: {start_date.date()} to {end_date.date()}")
    
    # Fetch carbon footprints for the period
    carbon_footprints = await db["carbon_footprints"].find({
        "user_id": user_id,
        "date": {
            "$gte": start_date,
            "$lte": end_date
        }
    }).sort("date", 1).to_list(length=days)
    
    print(f"   Found {len(carbon_footprints)} carbon footprints")
    
    # Generate all charts
    chart_service = ChartService()
    charts_data = chart_service.generate_all_charts(carbon_footprints)
    
    return ChartsResponse(
        monthly_trend=charts_data["monthly_trend"],
        category_breakdown=charts_data["category_breakdown"],
        weekly_comparison=charts_data["weekly_comparison"]
    )
