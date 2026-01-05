"""
Seed Data for PlanetZero MongoDB Collections
One example document per collection for testing and development
"""
from datetime import datetime
from bson import ObjectId


# ============================================================================
# SEED DATA - Example documents for each collection
# ============================================================================

SEED_DATA = {
    # ========================================================================
    # COLLECTION 1: USERS
    # ========================================================================
    "users": [
        {
            "_id": ObjectId("65a000000000000000000001"),
            "name": "Ravi Kumar",
            "email": "ravi.kumar@example.com",
            "phone": "+919876543210",
            "hashed_password": "$2b$12$6ie5A2GJmB7goKi80YmauuYBSB8lTq2uiOf1JEthrO0U2clu3Xyc2",  # "Password123"
            "role": "user",
            "is_active": True,
            "created_at": datetime(2026, 1, 1, 10, 0, 0),
            "updated_at": datetime(2026, 1, 4, 15, 30, 0),
            "last_login": datetime(2026, 1, 4, 9, 0, 0)
        },
        {
            "_id": ObjectId("65a000000000000000000002"),
            "name": "Priya Sharma",
            "email": "priya.sharma@example.com",
            "phone": "+919123456789",
            "hashed_password": "$2b$12$6ie5A2GJmB7goKi80YmauuYBSB8lTq2uiOf1JEthrO0U2clu3Xyc2",  # "Password123"
            "role": "user",
            "is_active": True,
            "created_at": datetime(2025, 12, 28, 14, 0, 0),
            "updated_at": datetime(2026, 1, 3, 18, 0, 0),
            "last_login": datetime(2026, 1, 3, 18, 0, 0)
        },
        {
            "_id": ObjectId("65a000000000000000000003"),
            "name": "Admin User",
            "email": "admin@planetzero.com",
            "phone": None,
            "hashed_password": "$2b$12$6ie5A2GJmB7goKi80YmauuYBSB8lTq2uiOf1JEthrO0U2clu3Xyc2",  # "Password123"
            "role": "admin",
            "is_active": True,
            "created_at": datetime(2025, 12, 1, 0, 0, 0),
            "updated_at": datetime(2026, 1, 4, 12, 0, 0),
            "last_login": datetime(2026, 1, 4, 12, 0, 0)
        }
    ],
    
    # ========================================================================
    # COLLECTION 2: USER_CONSENTS
    # ========================================================================
    "user_consents": [
        {
            "_id": ObjectId("65a100000000000000000001"),
            "user_id": ObjectId("65a000000000000000000001"),
            "consent_version": "v1.0",
            "accepted": True,
            "accepted_at": datetime(2026, 1, 1, 10, 5, 0),
            "ip_address": "103.120.45.67",
            "created_at": datetime(2026, 1, 1, 10, 5, 0)
        },
        {
            "_id": ObjectId("65a100000000000000000002"),
            "user_id": ObjectId("65a000000000000000000002"),
            "consent_version": "v1.0",
            "accepted": True,
            "accepted_at": datetime(2025, 12, 28, 14, 10, 0),
            "ip_address": "103.120.45.68",
            "created_at": datetime(2025, 12, 28, 14, 10, 0)
        }
    ],
    
    # ========================================================================
    # COLLECTION 3: PROFILES
    # ========================================================================
    "profiles": [
        {
            "_id": ObjectId("65a200000000000000000001"),
            "user_id": ObjectId("65a000000000000000000001"),
            "age_range": "26-35",
            "city": "Mumbai",
            "country": "India",
            "diet_type": "veg",
            "household_size": 4,
            "vehicle_type": "car",
            "created_at": datetime(2026, 1, 1, 10, 10, 0),
            "updated_at": datetime(2026, 1, 2, 16, 0, 0)
        },
        {
            "_id": ObjectId("65a200000000000000000002"),
            "user_id": ObjectId("65a000000000000000000002"),
            "age_range": "18-25",
            "city": "Bangalore",
            "country": "India",
            "diet_type": "vegan",
            "household_size": 2,
            "vehicle_type": "bike",
            "created_at": datetime(2025, 12, 28, 14, 15, 0),
            "updated_at": datetime(2025, 12, 28, 14, 15, 0)
        }
    ],
    
    # ========================================================================
    # COLLECTION 4: DAILY_LOGS
    # ========================================================================
    "daily_logs": [
        {
            "_id": ObjectId("65a300000000000000000001"),
            "user_id": ObjectId("65a000000000000000000001"),
            "date": datetime(2026, 1, 4),  # Changed to datetime
            "transport": {
                "mode": "car",
                "distance_km": 25.5
            },
            "electricity_units": 12.3,
            "water_liters": 150.0,
            "food_category": "veg",
            "shopping_spend": 500.0,
            "created_at": datetime(2026, 1, 4, 20, 0, 0)
        },
        {
            "_id": ObjectId("65a300000000000000000002"),
            "user_id": ObjectId("65a000000000000000000002"),
            "date": datetime(2026, 1, 3),  # Changed to datetime
            "transport": {
                "mode": "bike",
                "distance_km": 8.0
            },
            "electricity_units": 5.2,
            "water_liters": 80.0,
            "food_category": "vegan",
            "shopping_spend": 200.0,
            "created_at": datetime(2026, 1, 3, 21, 0, 0)
        },
        {
            "_id": ObjectId("65a300000000000000000003"),
            "user_id": ObjectId("65a000000000000000000001"),
            "date": datetime(2026, 1, 3),  # Changed to datetime
            "transport": {
                "mode": "metro",
                "distance_km": 18.0
            },
            "electricity_units": 10.5,
            "water_liters": 140.0,
            "food_category": "veg",
            "shopping_spend": 300.0,
            "created_at": datetime(2026, 1, 3, 20, 30, 0)
        }
    ],
    
    # ========================================================================
    # COLLECTION 5: EMISSION_FACTORS
    # ========================================================================
    "emission_factors": [
        {
            "_id": ObjectId("65a400000000000000000001"),
            "category": "transport",
            "type": "petrol_car",
            "unit": "km",
            "co2e_per_unit": 0.192,
            "region": "India",
            "source": "IPCC 2023 Guidelines",
            "updated_at": datetime(2026, 1, 1, 0, 0, 0)
        },
        {
            "_id": ObjectId("65a400000000000000000002"),
            "category": "energy",
            "type": "grid_electricity",
            "unit": "kWh",
            "co2e_per_unit": 0.82,
            "region": "India",
            "source": "Central Electricity Authority 2023",
            "updated_at": datetime(2026, 1, 1, 0, 0, 0)
        },
        {
            "_id": ObjectId("65a400000000000000000003"),
            "category": "food",
            "type": "vegetarian_meal",
            "unit": "meal",
            "co2e_per_unit": 2.0,
            "region": "Global",
            "source": "Our World in Data 2023",
            "updated_at": datetime(2026, 1, 1, 0, 0, 0)
        },
        {
            "_id": ObjectId("65a400000000000000000004"),
            "category": "transport",
            "type": "metro",
            "unit": "km",
            "co2e_per_unit": 0.041,
            "region": "India",
            "source": "IPCC 2023 Guidelines",
            "updated_at": datetime(2026, 1, 1, 0, 0, 0)
        },
        {
            "_id": ObjectId("65a400000000000000000005"),
            "category": "food",
            "type": "vegan_meal",
            "unit": "meal",
            "co2e_per_unit": 1.5,
            "region": "Global",
            "source": "Our World in Data 2023",
            "updated_at": datetime(2026, 1, 1, 0, 0, 0)
        }
    ],
    
    # ========================================================================
    # COLLECTION 6: CARBON_FOOTPRINTS
    # ========================================================================
    "carbon_footprints": [
        {
            "_id": ObjectId("65a500000000000000000001"),
            "user_id": ObjectId("65a000000000000000000001"),
            "date": datetime(2026, 1, 4),
            "total_emissions": 15.8,
            "transport_emissions": 4.9,
            "energy_emissions": 10.1,
            "food_emissions": 0.8,
            "comparison_to_average": -12.5,
            "created_at": datetime(2026, 1, 4, 21, 0, 0)
        },
        {
            "_id": ObjectId("65a500000000000000000002"),
            "user_id": ObjectId("65a000000000000000000002"),
            "date": datetime(2026, 1, 3),
            "total_emissions": 5.9,
            "transport_emissions": 0.0,
            "energy_emissions": 4.3,
            "food_emissions": 1.6,
            "comparison_to_average": -45.8,
            "created_at": datetime(2026, 1, 3, 22, 0, 0)
        },
        {
            "_id": ObjectId("65a500000000000000000003"),
            "user_id": ObjectId("65a000000000000000000001"),
            "date": datetime(2026, 1, 3),
            "total_emissions": 11.4,
            "transport_emissions": 0.7,
            "energy_emissions": 8.6,
            "food_emissions": 2.1,
            "comparison_to_average": -20.3,
            "created_at": datetime(2026, 1, 3, 21, 30, 0)
        }
    ],
    
    # ========================================================================
    # COLLECTION 7: RECOMMENDATIONS
    # ========================================================================
    "recommendations": [
        {
            "_id": ObjectId("65a600000000000000000001"),
            "user_id": ObjectId("65a000000000000000000001"),
            "category": "transport",
            "message": "Switch to metro for your daily commute to reduce emissions by 60%",
            "impact_score": 8,
            "is_applied": False,
            "created_at": datetime(2026, 1, 4, 10, 0, 0)
        },
        {
            "_id": ObjectId("65a600000000000000000002"),
            "user_id": ObjectId("65a000000000000000000001"),
            "category": "energy",
            "message": "Install LED bulbs to save 15% on electricity consumption",
            "impact_score": 6,
            "is_applied": True,
            "created_at": datetime(2026, 1, 3, 12, 0, 0)
        },
        {
            "_id": ObjectId("65a600000000000000000003"),
            "user_id": ObjectId("65a000000000000000000002"),
            "category": "food",
            "message": "Great job on your vegan diet! You're saving 3.5 kg CO2e per day",
            "impact_score": 9,
            "is_applied": True,
            "created_at": datetime(2026, 1, 2, 14, 0, 0)
        }
    ],
    
    # ========================================================================
    # COLLECTION 8: LEADERBOARD
    # ========================================================================
    "leaderboard": [
        {
            "_id": ObjectId("65a700000000000000000001"),
            "period": "weekly",
            "user_id": ObjectId("65a000000000000000000002"),
            "score": 41.3,
            "rank": 1,
            "calculated_at": datetime(2026, 1, 4, 0, 0, 0)
        },
        {
            "_id": ObjectId("65a700000000000000000002"),
            "period": "weekly",
            "user_id": ObjectId("65a000000000000000000001"),
            "score": 85.3,
            "rank": 42,
            "calculated_at": datetime(2026, 1, 4, 0, 0, 0)
        },
        {
            "_id": ObjectId("65a700000000000000000003"),
            "period": "monthly",
            "user_id": ObjectId("65a000000000000000000002"),
            "score": 180.5,
            "rank": 3,
            "calculated_at": datetime(2026, 1, 1, 0, 0, 0)
        }
    ],
    
    # ========================================================================
    # COLLECTION 9: COMMUNITY_POSTS
    # ========================================================================
    "community_posts": [
        {
            "_id": ObjectId("65a800000000000000000001"),
            "user_id": ObjectId("65a000000000000000000001"),
            "content": "Just completed my first week of cycling to work! Feeling great and helping the planet 🌍🚴‍♂️",
            "likes_count": 23,
            "comments_count": 5,
            "created_at": datetime(2026, 1, 4, 9, 0, 0),
            "updated_at": datetime(2026, 1, 4, 9, 0, 0)
        },
        {
            "_id": ObjectId("65a800000000000000000002"),
            "user_id": ObjectId("65a000000000000000000002"),
            "content": "Pro tip: Switching to a vegan diet reduced my carbon footprint by 40%! 🌱",
            "likes_count": 45,
            "comments_count": 12,
            "created_at": datetime(2026, 1, 3, 15, 0, 0),
            "updated_at": datetime(2026, 1, 3, 15, 0, 0)
        }
    ],
    
    # ========================================================================
    # COLLECTION 10: COMMUNITY_COMMENTS
    # ========================================================================
    "community_comments": [
        {
            "_id": ObjectId("65a900000000000000000001"),
            "post_id": ObjectId("65a800000000000000000001"),
            "user_id": ObjectId("65a000000000000000000002"),
            "comment": "That's awesome! How many km is your commute?",
            "created_at": datetime(2026, 1, 4, 10, 0, 0)
        },
        {
            "_id": ObjectId("65a900000000000000000002"),
            "post_id": ObjectId("65a800000000000000000001"),
            "user_id": ObjectId("65a000000000000000000001"),
            "comment": "About 8 km each way. Takes 30 minutes but totally worth it!",
            "created_at": datetime(2026, 1, 4, 10, 15, 0)
        },
        {
            "_id": ObjectId("65a900000000000000000003"),
            "post_id": ObjectId("65a800000000000000000002"),
            "user_id": ObjectId("65a000000000000000000001"),
            "comment": "Impressive! What's your favorite vegan recipe?",
            "created_at": datetime(2026, 1, 3, 16, 0, 0)
        }
    ],
    
    # ========================================================================
    # COLLECTION 11: ACTIVITY_HISTORY
    # ========================================================================
    "activity_history": [
        {
            "_id": ObjectId("65aa00000000000000000001"),
            "user_id": ObjectId("65a000000000000000000001"),
            "action": "login",
            "metadata": {
                "ip_address": "103.120.45.67",
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            },
            "timestamp": datetime(2026, 1, 4, 9, 0, 0)
        },
        {
            "_id": ObjectId("65aa00000000000000000002"),
            "user_id": ObjectId("65a000000000000000000001"),
            "action": "submit_daily_log",
            "metadata": {
                "date": "2026-01-04",
                "categories": ["transport", "energy", "food"]
            },
            "timestamp": datetime(2026, 1, 4, 20, 0, 0)
        },
        {
            "_id": ObjectId("65aa00000000000000000003"),
            "user_id": ObjectId("65a000000000000000000002"),
            "action": "update_profile",
            "metadata": {
                "changed_fields": ["diet_type"],
                "old_value": "veg",
                "new_value": "vegan"
            },
            "timestamp": datetime(2026, 1, 2, 11, 0, 0)
        }
    ],
    
    # ========================================================================
    # COLLECTION 12: NOTIFICATIONS
    # ========================================================================
    "notifications": [
        {
            "_id": ObjectId("65ab00000000000000000001"),
            "user_id": ObjectId("65a000000000000000000001"),
            "type": "achievement",
            "message": "Congratulations! You've reduced your carbon footprint by 20% this week!",
            "is_read": False,
            "created_at": datetime(2026, 1, 4, 18, 0, 0)
        },
        {
            "_id": ObjectId("65ab00000000000000000002"),
            "user_id": ObjectId("65a000000000000000000001"),
            "type": "reminder",
            "message": "Don't forget to log your daily activities!",
            "is_read": True,
            "created_at": datetime(2026, 1, 3, 19, 0, 0)
        },
        {
            "_id": ObjectId("65ab00000000000000000003"),
            "user_id": ObjectId("65a000000000000000000002"),
            "type": "social",
            "message": "Ravi Kumar commented on your post",
            "is_read": False,
            "created_at": datetime(2026, 1, 3, 16, 0, 0)
        }
    ]
}


# ============================================================================
# SEED SCRIPT
# ============================================================================

async def seed_database(db):
    """
    Insert seed data into all collections.
    Should only be run once during initial setup or testing.
    """
    for collection_name, documents in SEED_DATA.items():
        collection = db[collection_name]
        
        # Clear existing data (optional - comment out for production)
        await collection.delete_many({})
        
        # Insert seed documents
        if documents:
            await collection.insert_many(documents)
            print(f"✅ Seeded {len(documents)} documents into '{collection_name}'")
    
    print("\n🎉 Database seeded successfully!")


async def clear_database(db):
    """
    Clear all collections.
    Use with caution - only for development/testing!
    """
    for collection_name in SEED_DATA.keys():
        collection = db[collection_name]
        result = await collection.delete_many({})
        print(f"🗑️  Cleared {result.deleted_count} documents from '{collection_name}'")
    
    print("\n✅ Database cleared!")
