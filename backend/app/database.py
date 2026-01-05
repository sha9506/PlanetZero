from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    client: AsyncIOMotorClient = None
    db = None

db = Database()

async def connect_to_mongo():
    """Connect to MongoDB"""
    try:
        db.client = AsyncIOMotorClient(
            os.getenv("MONGODB_URL", "mongodb://localhost:27017"),
            server_api=ServerApi('1')
        )
        db.db = db.client[os.getenv("DATABASE_NAME", "planetzero")]
        
        # Test connection
        await db.client.admin.command('ping')
        print("✅ Connected to MongoDB successfully")
    except Exception as e:
        print(f"❌ Error connecting to MongoDB: {e}")
        raise

async def close_mongo_connection():
    """Close MongoDB connection"""
    if db.client:
        db.client.close()
        print("✅ MongoDB connection closed")

def get_database():
    """Get database instance"""
    return db.db

# Collection names
USERS_COLLECTION = "users"
ACTIVITIES_COLLECTION = "activities"
RECOMMENDATIONS_COLLECTION = "recommendations"
COMMUNITIES_COLLECTION = "communities"
COMMUNITY_MEMBERS_COLLECTION = "community_members"
BADGES_COLLECTION = "badges"
USER_BADGES_COLLECTION = "user_badges"
NOTIFICATIONS_COLLECTION = "notifications"
DAILY_LOGS_COLLECTION = "daily_logs"
