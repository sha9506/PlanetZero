"""
Recommendations Routes
Provides personalized recommendations based on user's emission patterns
"""
from fastapi import APIRouter, HTTPException, status, Depends
from database import get_database, DAILY_LOGS_COLLECTION
from schemas import RecommendationsResponse, Recommendation
from routes.auth import get_current_user
from services.recommendation_service import generate_recommendations, calculate_total_savings
from datetime import datetime, timedelta

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])

@router.get("", response_model=RecommendationsResponse)
async def get_recommendations(current_user=Depends(get_current_user)):
    """
    Get personalized recommendations based on user's emission patterns
    
    Analyzes last 30 days of data and provides:
    - Top 5 actionable recommendations
    - Potential carbon savings
    - Focus on highest emission category
    """
    db = get_database()
    user_id = str(current_user["_id"])
    
    # Get last 30 days of logs
    today = datetime.utcnow().date()
    month_ago = (today - timedelta(days=29)).strftime('%Y-%m-%d')
    today_str = today.strftime('%Y-%m-%d')
    
    logs = await db[DAILY_LOGS_COLLECTION].find({
        "user_id": user_id,
        "date": {"$gte": month_ago, "$lte": today_str}
    }).to_list(length=100)
    
    if not logs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No emission data found. Please log your daily activities first."
        )
    
    # Calculate average emissions across categories
    total_transport = sum(log.get("transport_emissions", 0) for log in logs)
    total_electricity = sum(log.get("electricity_emissions", 0) for log in logs)
    total_food = sum(log.get("food_emissions", 0) for log in logs)
    total_lifestyle = sum(log.get("lifestyle_emissions", 0) for log in logs)
    
    num_days = len(logs)
    avg_transport = total_transport / num_days
    avg_electricity = total_electricity / num_days
    avg_food = total_food / num_days
    avg_lifestyle = total_lifestyle / num_days
    
    # Determine highest emission category
    categories = {
        "transportation": avg_transport,
        "electricity": avg_electricity,
        "food": avg_food,
        "lifestyle": avg_lifestyle
    }
    highest_category = max(categories, key=categories.get)
    
    # Generate recommendations
    recommendations_data = generate_recommendations(
        highest_category=highest_category,
        transport_emissions=avg_transport,
        electricity_emissions=avg_electricity,
        food_emissions=avg_food,
        lifestyle_emissions=avg_lifestyle
    )
    
    # Convert to Pydantic models
    recommendations = [
        Recommendation(**rec) for rec in recommendations_data
    ]
    
    # Calculate total potential savings
    total_savings = calculate_total_savings(recommendations_data)
    
    return RecommendationsResponse(
        recommendations=recommendations,
        highest_emission_category=highest_category,
        total_potential_savings=total_savings
    )
