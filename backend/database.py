"""
Database Configuration for PlanetZero
Handles MongoDB connection and collection management
"""
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    client: AsyncIOMotorClient = None
    db = None

database = Database()

async def connect_to_mongo():
    """
    Establish connection to MongoDB
    """
    try:
        database.client = AsyncIOMotorClient(
            os.getenv("MONGODB_URL", "mongodb://localhost:27017")
        )
        database.db = database.client[os.getenv("DATABASE_NAME", "planetzero")]
        
        # Test connection
        await database.client.admin.command('ping')
        print("✅ Connected to MongoDB successfully")
    except ConnectionFailure as e:
        print(f"❌ Failed to connect to MongoDB: {e}")
        raise

async def close_mongo_connection():
    """
    Close MongoDB connection
    """
    if database.client:
        database.client.close()
        print("✅ MongoDB connection closed")

def get_database():
    """
    Get database instance
    """
    return database.db

# Collection names
USERS_COLLECTION = "users"
CONSENTS_COLLECTION = "consents"
DAILY_LOGS_COLLECTION = "daily_logs"
EMISSION_SUMMARIES_COLLECTION = "emission_summaries"
