"""
Carbon Emission Calculation Service
Implements the core logic for calculating carbon emissions based on user activities

Formula: Carbon Emission = Activity × Emission Factor
"""
from typing import List, Dict, Tuple

# ============ Emission Factors (kg CO₂) ============

# Transportation emission factors (kg CO₂ per km)
TRANSPORT_EMISSION_FACTORS = {
    "car_petrol": 0.192,      # Petrol car
    "car_diesel": 0.171,      # Diesel car
    "bus": 0.089,             # Public bus
    "train": 0.041,           # Train/metro
    "flight": 0.255,          # Flight (short-haul average)
}

# Electricity emission factor (kg CO₂ per kWh)
# India's average grid emission factor
ELECTRICITY_EMISSION_FACTOR = 0.82

# Food emission factors (kg CO₂ per meal)
FOOD_EMISSION_FACTORS = {
    "veg": 2.0,               # Vegetarian meal
    "non_veg": 5.5,           # Non-vegetarian meal
    "vegan": 1.5,             # Vegan meal
}

# Lifestyle emission factors (kg CO₂ per item)
LIFESTYLE_EMISSION_FACTORS = {
    "clothing": 6.0,          # Average per clothing item
    "electronics": 50.0,      # Average per electronic item
}

def calculate_transport_emissions(transportation_data: List[Dict]) -> Tuple[float, List[Dict]]:
    """
    Calculate total transportation emissions
    
    Formula: Emission = Distance (km) × Emission Factor (kg CO₂/km)
    
    Args:
        transportation_data: List of transportation entries
            Each entry: {"mode": str, "distance_km": float}
    
    Returns:
        Tuple of (total_emissions, detailed_entries)
    """
    total_emissions = 0.0
    detailed_entries = []
    
    for entry in transportation_data:
        mode = entry.get("mode")
        distance_km = entry.get("distance_km", 0)
        
        # Get emission factor for this mode
        emission_factor = TRANSPORT_EMISSION_FACTORS.get(mode, 0)
        
        # Calculate emissions for this trip
        emissions = distance_km * emission_factor
        
        total_emissions += emissions
        
        # Store detailed entry
        detailed_entries.append({
            "mode": mode,
            "distance_km": distance_km,
            "emission_factor": emission_factor,
            "emissions": round(emissions, 3)
        })
    
    return round(total_emissions, 3), detailed_entries

def calculate_electricity_emissions(electricity_kwh: float) -> float:
    """
    Calculate electricity consumption emissions
    
    Formula: Emission = Electricity (kWh) × Emission Factor (kg CO₂/kWh)
    
    Args:
        electricity_kwh: Electricity consumption in kWh
    
    Returns:
        Total electricity emissions in kg CO₂
    """
    emissions = electricity_kwh * ELECTRICITY_EMISSION_FACTOR
    return round(emissions, 3)

def calculate_food_emissions(food_data: List[Dict]) -> Tuple[float, List[Dict]]:
    """
    Calculate total food emissions
    
    Formula: Emission = Meals Count × Emission Factor (kg CO₂/meal)
    
    Args:
        food_data: List of food entries
            Each entry: {"meal_type": str, "meals_count": int}
    
    Returns:
        Tuple of (total_emissions, detailed_entries)
    """
    total_emissions = 0.0
    detailed_entries = []
    
    for entry in food_data:
        meal_type = entry.get("meal_type")
        meals_count = entry.get("meals_count", 0)
        
        # Get emission factor for this meal type
        emission_factor = FOOD_EMISSION_FACTORS.get(meal_type, 0)
        
        # Calculate emissions for these meals
        emissions = meals_count * emission_factor
        
        total_emissions += emissions
        
        # Store detailed entry
        detailed_entries.append({
            "meal_type": meal_type,
            "meals_count": meals_count,
            "emission_factor": emission_factor,
            "emissions": round(emissions, 3)
        })
    
    return round(total_emissions, 3), detailed_entries

def calculate_lifestyle_emissions(lifestyle_data: List[Dict]) -> Tuple[float, List[Dict]]:
    """
    Calculate total lifestyle emissions
    
    Formula: Emission = Items Count × Emission Factor (kg CO₂/item)
    
    Args:
        lifestyle_data: List of lifestyle entries
            Each entry: {"category": str, "items_count": int}
    
    Returns:
        Tuple of (total_emissions, detailed_entries)
    """
    total_emissions = 0.0
    detailed_entries = []
    
    for entry in lifestyle_data:
        category = entry.get("category")
        items_count = entry.get("items_count", 0)
        
        # Get emission factor for this category
        emission_factor = LIFESTYLE_EMISSION_FACTORS.get(category, 0)
        
        # Calculate emissions for these items
        emissions = items_count * emission_factor
        
        total_emissions += emissions
        
        # Store detailed entry
        detailed_entries.append({
            "category": category,
            "items_count": items_count,
            "emission_factor": emission_factor,
            "emissions": round(emissions, 3)
        })
    
    return round(total_emissions, 3), detailed_entries

def calculate_total_emissions(
    transportation_data: List[Dict],
    electricity_kwh: float,
    food_data: List[Dict],
    lifestyle_data: List[Dict]
) -> Dict:
    """
    Calculate total emissions across all categories
    
    Args:
        transportation_data: List of transportation entries
        electricity_kwh: Electricity consumption
        food_data: List of food entries
        lifestyle_data: List of lifestyle entries
    
    Returns:
        Dictionary containing:
            - Category-wise emissions
            - Detailed breakdown
            - Total emissions
            - Highest emission category
    """
    # Calculate emissions for each category
    transport_emissions, transport_details = calculate_transport_emissions(transportation_data)
    electricity_emissions = calculate_electricity_emissions(electricity_kwh)
    food_emissions, food_details = calculate_food_emissions(food_data)
    lifestyle_emissions, lifestyle_details = calculate_lifestyle_emissions(lifestyle_data)
    
    # Calculate total
    total_emissions = (
        transport_emissions +
        electricity_emissions +
        food_emissions +
        lifestyle_emissions
    )
    
    # Determine highest emission category
    categories = {
        "transportation": transport_emissions,
        "electricity": electricity_emissions,
        "food": food_emissions,
        "lifestyle": lifestyle_emissions
    }
    highest_category = max(categories, key=categories.get)
    
    return {
        "transport_emissions": transport_emissions,
        "electricity_emissions": electricity_emissions,
        "food_emissions": food_emissions,
        "lifestyle_emissions": lifestyle_emissions,
        "total_emissions": round(total_emissions, 3),
        "highest_category": highest_category,
        "transport_details": transport_details,
        "food_details": food_details,
        "lifestyle_details": lifestyle_details
    }

def get_emission_factors() -> Dict:
    """
    Get all emission factors for reference
    
    Returns:
        Dictionary containing all emission factors
    """
    return {
        "transportation": TRANSPORT_EMISSION_FACTORS,
        "electricity": ELECTRICITY_EMISSION_FACTOR,
        "food": FOOD_EMISSION_FACTORS,
        "lifestyle": LIFESTYLE_EMISSION_FACTORS
    }
