"""
Dashboard Routes
Provides summary statistics for today, weekly, and monthly emissions
"""
from fastapi import APIRouter, HTTPException, status, Depends
from database import get_database, DAILY_LOGS_COLLECTION
from schemas import DashboardSummary, DashboardResponse
from routes.auth import get_current_user
from datetime import datetime, timedelta

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

async def calculate_period_summary(
    db,
    user_id: str,
    start_date: str,
    end_date: str,
    period_name: str
) -> DashboardSummary:
    """
    Calculate emission summary for a given period
    
    Args:
        db: Database connection
        user_id: User ID
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
        period_name: Period label (today, weekly, monthly)
    
    Returns:
        DashboardSummary object with aggregated data
    """
    # Fetch logs for the period
    logs = await db[DAILY_LOGS_COLLECTION].find({
        "user_id": user_id,
        "date": {"$gte": start_date, "$lte": end_date}
    }).to_list(length=100)
    
    if not logs:
        # Return zero emissions if no logs found
        return DashboardSummary(
            period=period_name,
            total_emissions=0.0,
            transport_emissions=0.0,
            electricity_emissions=0.0,
            food_emissions=0.0,
            lifestyle_emissions=0.0,
            average_daily_emissions=0.0,
            highest_category="none"
        )
    
    # Aggregate emissions
    total_transport = sum(log.get("transport_emissions", 0) for log in logs)
    total_electricity = sum(log.get("electricity_emissions", 0) for log in logs)
    total_food = sum(log.get("food_emissions", 0) for log in logs)
    total_lifestyle = sum(log.get("lifestyle_emissions", 0) for log in logs)
    total_emissions = total_transport + total_electricity + total_food + total_lifestyle
    
    # Calculate average
    num_days = len(logs)
    average_daily = total_emissions / num_days if num_days > 0 else 0.0
    
    # Find highest category
    categories = {
        "transportation": total_transport,
        "electricity": total_electricity,
        "food": total_food,
        "lifestyle": total_lifestyle
    }
    highest_category = max(categories, key=categories.get) if total_emissions > 0 else "none"
    
    return DashboardSummary(
        period=period_name,
        total_emissions=round(total_emissions, 3),
        transport_emissions=round(total_transport, 3),
        electricity_emissions=round(total_electricity, 3),
        food_emissions=round(total_food, 3),
        lifestyle_emissions=round(total_lifestyle, 3),
        average_daily_emissions=round(average_daily, 3),
        highest_category=highest_category
    )

@router.get("", response_model=DashboardResponse)
async def get_dashboard(current_user=Depends(get_current_user)):
    """
    Get dashboard with today, weekly, and monthly emission summaries
    
    Returns aggregated emissions for:
    - Today
    - Last 7 days
    - Last 30 days
    """
    db = get_database()
    user_id = str(current_user["_id"])
    
    # Calculate dates
    today = datetime.utcnow().date()
    today_str = today.strftime('%Y-%m-%d')
    
    week_ago = today - timedelta(days=6)
    week_ago_str = week_ago.strftime('%Y-%m-%d')
    
    month_ago = today - timedelta(days=29)
    month_ago_str = month_ago.strftime('%Y-%m-%d')
    
    # Get summaries for each period
    today_summary = await calculate_period_summary(
        db, user_id, today_str, today_str, "today"
    )
    
    weekly_summary = await calculate_period_summary(
        db, user_id, week_ago_str, today_str, "weekly"
    )
    
    monthly_summary = await calculate_period_summary(
        db, user_id, month_ago_str, today_str, "monthly"
    )
    
    return DashboardResponse(
        today=today_summary,
        weekly=weekly_summary,
        monthly=monthly_summary
    )
