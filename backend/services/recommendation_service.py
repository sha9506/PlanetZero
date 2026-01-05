"""
Recommendation Service
Generates personalized recommendations based on user's emission patterns

Uses rule-based logic to suggest actions for reducing carbon footprint
"""
from typing import List, Dict

def generate_recommendations(
    highest_category: str,
    transport_emissions: float,
    electricity_emissions: float,
    food_emissions: float,
    lifestyle_emissions: float
) -> List[Dict]:
    """
    Generate personalized recommendations based on emission patterns
    
    Args:
        highest_category: Category with highest emissions
        transport_emissions: Transport emissions in kg CO₂
        electricity_emissions: Electricity emissions in kg CO₂
        food_emissions: Food emissions in kg CO₂
        lifestyle_emissions: Lifestyle emissions in kg CO₂
    
    Returns:
        List of recommendation dictionaries
    """
    recommendations = []
    
    # ============ Transportation Recommendations ============
    if highest_category == "transportation" or transport_emissions > 10:
        recommendations.extend([
            {
                "category": "transportation",
                "title": "Switch to Public Transport",
                "description": "Use buses or trains instead of private vehicles. Public transport can reduce your carbon footprint by up to 45% per km.",
                "potential_savings_kg": round(transport_emissions * 0.45, 2)
            },
            {
                "category": "transportation",
                "title": "Carpool or Bike",
                "description": "Share rides with colleagues or use a bicycle for short distances. Carpooling can cut emissions by 50%.",
                "potential_savings_kg": round(transport_emissions * 0.50, 2)
            },
            {
                "category": "transportation",
                "title": "Work from Home",
                "description": "If possible, work remotely 1-2 days a week to reduce commute emissions significantly.",
                "potential_savings_kg": round(transport_emissions * 0.30, 2)
            }
        ])
    
    # ============ Electricity Recommendations ============
    if highest_category == "electricity" or electricity_emissions > 8:
        recommendations.extend([
            {
                "category": "electricity",
                "title": "Optimize AC Usage",
                "description": "Set AC to 24°C instead of 18°C and use fans. This can reduce electricity consumption by 30-40%.",
                "potential_savings_kg": round(electricity_emissions * 0.35, 2)
            },
            {
                "category": "electricity",
                "title": "LED Lighting",
                "description": "Replace all bulbs with LED lights. LEDs use 75% less energy than traditional bulbs.",
                "potential_savings_kg": round(electricity_emissions * 0.15, 2)
            },
            {
                "category": "electricity",
                "title": "Unplug Devices",
                "description": "Unplug chargers and devices when not in use. Phantom power can account for 10% of electricity bills.",
                "potential_savings_kg": round(electricity_emissions * 0.10, 2)
            },
            {
                "category": "electricity",
                "title": "Energy-Efficient Appliances",
                "description": "Use 5-star rated appliances and maintain them regularly for optimal efficiency.",
                "potential_savings_kg": round(electricity_emissions * 0.20, 2)
            }
        ])
    
    # ============ Food Recommendations ============
    if highest_category == "food" or food_emissions > 15:
        recommendations.extend([
            {
                "category": "food",
                "title": "Adopt Plant-Based Meals",
                "description": "Try Meatless Mondays or replace 2-3 non-veg meals per week with vegetarian options. Can reduce food emissions by 60%.",
                "potential_savings_kg": round(food_emissions * 0.60, 2)
            },
            {
                "category": "food",
                "title": "Choose Local and Seasonal",
                "description": "Buy locally grown, seasonal produce to reduce transportation and storage emissions.",
                "potential_savings_kg": round(food_emissions * 0.25, 2)
            },
            {
                "category": "food",
                "title": "Reduce Food Waste",
                "description": "Plan meals, store food properly, and compost scraps. Food waste contributes 8% of global emissions.",
                "potential_savings_kg": round(food_emissions * 0.15, 2)
            }
        ])
    
    # ============ Lifestyle Recommendations ============
    if highest_category == "lifestyle" or lifestyle_emissions > 20:
        recommendations.extend([
            {
                "category": "lifestyle",
                "title": "Buy Second-Hand",
                "description": "Purchase pre-owned clothing and electronics. Manufacturing new items has high carbon costs.",
                "potential_savings_kg": round(lifestyle_emissions * 0.70, 2)
            },
            {
                "category": "lifestyle",
                "title": "Repair Before Replace",
                "description": "Repair broken items instead of buying new ones. Extends product life and reduces waste.",
                "potential_savings_kg": round(lifestyle_emissions * 0.50, 2)
            },
            {
                "category": "lifestyle",
                "title": "Minimalist Approach",
                "description": "Practice mindful consumption. Ask 'Do I really need this?' before every purchase.",
                "potential_savings_kg": round(lifestyle_emissions * 0.40, 2)
            }
        ])
    
    # ============ General Recommendations (if emissions are low) ============
    if len(recommendations) == 0:
        recommendations.extend([
            {
                "category": "general",
                "title": "Great Job!",
                "description": "You're already maintaining a low carbon footprint. Keep up the good work!",
                "potential_savings_kg": 0.0
            },
            {
                "category": "general",
                "title": "Spread Awareness",
                "description": "Share your eco-friendly habits with friends and family to multiply your impact.",
                "potential_savings_kg": 0.0
            },
            {
                "category": "general",
                "title": "Track Consistently",
                "description": "Continue logging daily to maintain your sustainable lifestyle and identify areas for improvement.",
                "potential_savings_kg": 0.0
            }
        ])
    
    # Return top recommendations based on highest category
    # Prioritize recommendations for the highest emission category
    sorted_recommendations = sorted(
        recommendations,
        key=lambda x: (
            x['category'] == highest_category,
            x['potential_savings_kg']
        ),
        reverse=True
    )
    
    return sorted_recommendations[:5]  # Return top 5 recommendations

def calculate_total_savings(recommendations: List[Dict]) -> float:
    """
    Calculate total potential savings from all recommendations
    
    Args:
        recommendations: List of recommendation dictionaries
    
    Returns:
        Total potential savings in kg CO₂
    """
    total_savings = sum(rec['potential_savings_kg'] for rec in recommendations)
    return round(total_savings, 2)
