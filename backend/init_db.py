"""
Script to initialize the database with default badges
Run this after starting MongoDB to populate initial data
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

load_dotenv()

# Badge data matching the frontend
BADGES = [
    {
        "name": "First Steps",
        "description": "Logged your first daily activity",
        "icon": "FaSeedling",
        "color": "gold"
    },
    {
        "name": "Week Warrior",
        "description": "Logged activities for 7 consecutive days",
        "icon": "FaFire",
        "color": "green"
    },
    {
        "name": "Eco Champion",
        "description": "Reduced carbon footprint by 20%",
        "icon": "FaTrophy",
        "color": "blue"
    },
    {
        "name": "Green Commuter",
        "description": "Used public transport 10 times",
        "icon": "FaBus",
        "color": "purple"
    },
    {
        "name": "Energy Saver",
        "description": "Reduced energy consumption by 30%",
        "icon": "FaBolt",
        "color": "orange"
    },
    {
        "name": "Zero Waste Hero",
        "description": "Completed 5 recycling tasks",
        "icon": "FaRecycle",
        "color": "teal"
    },
    {
        "name": "Team Player",
        "description": "Joined 3 communities",
        "icon": "FaHandshake",
        "color": "pink"
    },
    {
        "name": "100-Day Streak",
        "description": "Logged activities for 100 days",
        "icon": "FaMedal",
        "color": "indigo"
    },
    {
        "name": "Community Founder",
        "description": "Created your own community",
        "icon": "FaUsers",
        "color": "emerald"
    }
]

async def init_badges():
    """Initialize badges in database"""
    try:
        # Connect to MongoDB
        client = AsyncIOMotorClient(
            os.getenv("MONGODB_URL", "mongodb://localhost:27017"),
            server_api=ServerApi('1')
        )
        db = client[os.getenv("DATABASE_NAME", "planetzero")]
        
        print("🔌 Connected to MongoDB")
        
        # Check if badges already exist
        existing_count = await db.badges.count_documents({})
        
        if existing_count > 0:
            print(f"⚠️  Database already has {existing_count} badges")
            response = input("Do you want to reset badges? (yes/no): ")
            if response.lower() == 'yes':
                await db.badges.delete_many({})
                print("🗑️  Deleted existing badges")
            else:
                print("✅ Keeping existing badges")
                client.close()
                return
        
        # Insert badges
        result = await db.badges.insert_many(BADGES)
        print(f"✅ Inserted {len(result.inserted_ids)} badges")
        
        # Display inserted badges
        cursor = db.badges.find({})
        badges = await cursor.to_list(length=None)
        
        print("\n📛 Badges in database:")
        for badge in badges:
            print(f"  - {badge['name']}: {badge['description']}")
        
        client.close()
        print("\n✅ Database initialization complete!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(init_badges())
