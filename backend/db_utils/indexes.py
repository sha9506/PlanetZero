"""
MongoDB Index Creation for PlanetZero
Creates all necessary indexes for optimal query performance
"""
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import IndexModel, ASCENDING, DESCENDING


async def create_all_indexes(db: AsyncIOMotorDatabase):
    """
    Create all collection indexes.
    Should be run on application startup or via migration script.
    """
    
    # ============================================================================
    # COLLECTION 1: USERS
    # ============================================================================
    await db.users.create_indexes([
        IndexModel(
            [("email", ASCENDING)],
            unique=True,
            name="idx_email_unique"
        ),
        IndexModel(
            [("role", ASCENDING)],
            name="idx_role"
        ),
        IndexModel(
            [("is_active", ASCENDING)],
            name="idx_is_active"
        ),
        IndexModel(
            [("created_at", DESCENDING)],
            name="idx_created_at"
        )
    ])
    print("✅ Created indexes for 'users' collection")
    
    # ============================================================================
    # COLLECTION 2: USER_CONSENTS
    # ============================================================================
    await db.user_consents.create_indexes([
        IndexModel(
            [("user_id", ASCENDING)],
            name="idx_user_id"
        ),
        IndexModel(
            [("consent_version", ASCENDING)],
            name="idx_consent_version"
        ),
        IndexModel(
            [("user_id", ASCENDING), ("consent_version", ASCENDING)],
            name="idx_user_consent_version"
        )
    ])
    print("✅ Created indexes for 'user_consents' collection")
    
    # ============================================================================
    # COLLECTION 3: PROFILES
    # ============================================================================
    await db.profiles.create_indexes([
        IndexModel(
            [("user_id", ASCENDING)],
            unique=True,
            name="idx_user_id_unique"
        ),
        IndexModel(
            [("city", ASCENDING)],
            name="idx_city"
        ),
        IndexModel(
            [("country", ASCENDING)],
            name="idx_country"
        ),
        IndexModel(
            [("diet_type", ASCENDING)],
            name="idx_diet_type"
        )
    ])
    print("✅ Created indexes for 'profiles' collection")
    
    # ============================================================================
    # COLLECTION 4: DAILY_LOGS
    # ============================================================================
    await db.daily_logs.create_indexes([
        IndexModel(
            [("user_id", ASCENDING), ("date", DESCENDING)],
            unique=True,
            name="idx_user_date_unique"
        ),
        IndexModel(
            [("date", DESCENDING)],
            name="idx_date"
        ),
        IndexModel(
            [("created_at", DESCENDING)],
            name="idx_created_at"
        )
    ])
    print("✅ Created indexes for 'daily_logs' collection")
    
    # ============================================================================
    # COLLECTION 5: EMISSION_FACTORS
    # ============================================================================
    await db.emission_factors.create_indexes([
        IndexModel(
            [("category", ASCENDING)],
            name="idx_category"
        ),
        IndexModel(
            [("region", ASCENDING)],
            name="idx_region"
        ),
        IndexModel(
            [("category", ASCENDING), ("type", ASCENDING), ("region", ASCENDING)],
            name="idx_category_type_region"
        ),
        IndexModel(
            [("updated_at", DESCENDING)],
            name="idx_updated_at"
        )
    ])
    print("✅ Created indexes for 'emission_factors' collection")
    
    # ============================================================================
    # COLLECTION 6: CARBON_FOOTPRINTS
    # ============================================================================
    await db.carbon_footprints.create_indexes([
        IndexModel(
            [("user_id", ASCENDING), ("date", DESCENDING)],
            unique=True,
            name="idx_user_date_unique"
        ),
        IndexModel(
            [("date", DESCENDING)],
            name="idx_date"
        ),
        IndexModel(
            [("total_emissions", DESCENDING)],
            name="idx_total_emissions"
        ),
        IndexModel(
            [("created_at", DESCENDING)],
            name="idx_created_at"
        )
    ])
    print("✅ Created indexes for 'carbon_footprints' collection")
    
    # ============================================================================
    # COLLECTION 7: RECOMMENDATIONS
    # ============================================================================
    await db.recommendations.create_indexes([
        IndexModel(
            [("user_id", ASCENDING)],
            name="idx_user_id"
        ),
        IndexModel(
            [("category", ASCENDING)],
            name="idx_category"
        ),
        IndexModel(
            [("is_applied", ASCENDING)],
            name="idx_is_applied"
        ),
        IndexModel(
            [("impact_score", DESCENDING)],
            name="idx_impact_score"
        ),
        IndexModel(
            [("user_id", ASCENDING), ("is_applied", ASCENDING)],
            name="idx_user_applied"
        )
    ])
    print("✅ Created indexes for 'recommendations' collection")
    
    # ============================================================================
    # COLLECTION 8: LEADERBOARD
    # ============================================================================
    await db.leaderboard.create_indexes([
        IndexModel(
            [("period", ASCENDING), ("rank", ASCENDING)],
            name="idx_period_rank"
        ),
        IndexModel(
            [("user_id", ASCENDING), ("period", ASCENDING)],
            name="idx_user_period"
        ),
        IndexModel(
            [("calculated_at", DESCENDING)],
            name="idx_calculated_at"
        ),
        IndexModel(
            [("period", ASCENDING), ("score", ASCENDING)],
            name="idx_period_score"
        )
    ])
    print("✅ Created indexes for 'leaderboard' collection")
    
    # ============================================================================
    # COLLECTION 9: COMMUNITY_POSTS
    # ============================================================================
    await db.community_posts.create_indexes([
        IndexModel(
            [("user_id", ASCENDING)],
            name="idx_user_id"
        ),
        IndexModel(
            [("created_at", DESCENDING)],
            name="idx_created_at"
        ),
        IndexModel(
            [("likes_count", DESCENDING)],
            name="idx_likes_count"
        ),
        IndexModel(
            [("comments_count", DESCENDING)],
            name="idx_comments_count"
        )
    ])
    print("✅ Created indexes for 'community_posts' collection")
    
    # ============================================================================
    # COLLECTION 10: COMMUNITY_COMMENTS
    # ============================================================================
    await db.community_comments.create_indexes([
        IndexModel(
            [("post_id", ASCENDING), ("created_at", ASCENDING)],
            name="idx_post_created"
        ),
        IndexModel(
            [("user_id", ASCENDING)],
            name="idx_user_id"
        ),
        IndexModel(
            [("created_at", DESCENDING)],
            name="idx_created_at"
        )
    ])
    print("✅ Created indexes for 'community_comments' collection")
    
    # ============================================================================
    # COLLECTION 11: ACTIVITY_HISTORY
    # ============================================================================
    await db.activity_history.create_indexes([
        IndexModel(
            [("user_id", ASCENDING), ("timestamp", DESCENDING)],
            name="idx_user_timestamp"
        ),
        IndexModel(
            [("action", ASCENDING)],
            name="idx_action"
        ),
        IndexModel(
            [("timestamp", DESCENDING)],
            name="idx_timestamp"
        )
    ])
    print("✅ Created indexes for 'activity_history' collection")
    
    # ============================================================================
    # COLLECTION 12: NOTIFICATIONS
    # ============================================================================
    await db.notifications.create_indexes([
        IndexModel(
            [("user_id", ASCENDING), ("is_read", ASCENDING)],
            name="idx_user_is_read"
        ),
        IndexModel(
            [("user_id", ASCENDING), ("created_at", DESCENDING)],
            name="idx_user_created"
        ),
        IndexModel(
            [("type", ASCENDING)],
            name="idx_type"
        ),
        IndexModel(
            [("created_at", DESCENDING)],
            name="idx_created_at"
        )
    ])
    print("✅ Created indexes for 'notifications' collection")
    
    print("\n🎉 All indexes created successfully!")


async def drop_all_indexes(db: AsyncIOMotorDatabase):
    """
    Drop all custom indexes (keeps _id index).
    Use with caution - only for development/testing.
    """
    collections = [
        'users', 'user_consents', 'profiles', 'daily_logs',
        'emission_factors', 'carbon_footprints', 'recommendations',
        'leaderboard', 'community_posts', 'community_comments',
        'activity_history', 'notifications'
    ]
    
    for collection_name in collections:
        collection = db[collection_name]
        # Drop all indexes except _id
        indexes = await collection.index_information()
        for index_name in indexes:
            if index_name != '_id_':
                await collection.drop_index(index_name)
        print(f"🗑️  Dropped indexes for '{collection_name}' collection")
    
    print("\n✅ All custom indexes dropped!")
