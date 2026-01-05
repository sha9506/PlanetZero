"""
Database Setup and Initialization Script for PlanetZero
Run this script to set up MongoDB collections, indexes, and seed data
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from db_utils.indexes import create_all_indexes, drop_all_indexes
from db_utils.seed_data import seed_database, clear_database


# MongoDB Configuration
MONGODB_URL = "mongodb://localhost:27017"
DATABASE_NAME = "planetzero_db"


async def setup_database():
    """
    Initialize MongoDB database with collections, indexes, and seed data.
    """
    print("🚀 Initializing PlanetZero Database...")
    print(f"📍 MongoDB URL: {MONGODB_URL}")
    print(f"📚 Database: {DATABASE_NAME}\n")
    
    # Connect to MongoDB
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DATABASE_NAME]
    
    try:
        # Test connection
        await client.admin.command('ping')
        print("✅ Connected to MongoDB successfully!\n")
        
        # Step 1: Create indexes
        print("=" * 60)
        print("STEP 1: Creating Indexes")
        print("=" * 60)
        await create_all_indexes(db)
        
        # Step 2: Seed database with sample data
        print("\n" + "=" * 60)
        print("STEP 2: Seeding Database")
        print("=" * 60)
        await seed_database(db)
        
        # Step 3: Verify collections
        print("\n" + "=" * 60)
        print("STEP 3: Verifying Collections")
        print("=" * 60)
        collections = await db.list_collection_names()
        print(f"\n📦 Total Collections: {len(collections)}")
        for collection_name in sorted(collections):
            count = await db[collection_name].count_documents({})
            print(f"   - {collection_name}: {count} documents")
        
        print("\n" + "=" * 60)
        print("🎉 Database initialization complete!")
        print("=" * 60)
        print("\n✨ You can now start the FastAPI application")
        
    except Exception as e:
        print(f"\n❌ Error during initialization: {e}")
        raise
    finally:
        client.close()
        print("\n🔒 Database connection closed")


async def reset_database():
    """
    Reset database: drop all data and reinitialize.
    USE WITH CAUTION - This will delete all data!
    """
    print("⚠️  WARNING: This will delete ALL data from the database!")
    print(f"📍 MongoDB URL: {MONGODB_URL}")
    print(f"📚 Database: {DATABASE_NAME}\n")
    
    confirm = input("Type 'DELETE ALL DATA' to confirm: ")
    if confirm != "DELETE ALL DATA":
        print("❌ Operation cancelled")
        return
    
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DATABASE_NAME]
    
    try:
        print("\n🗑️  Clearing database...")
        await clear_database(db)
        
        print("\n🗑️  Dropping indexes...")
        await drop_all_indexes(db)
        
        print("\n🔄 Reinitializing database...")
        await create_all_indexes(db)
        await seed_database(db)
        
        print("\n✅ Database reset complete!")
        
    except Exception as e:
        print(f"\n❌ Error during reset: {e}")
        raise
    finally:
        client.close()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "reset":
        # Run reset command
        asyncio.run(reset_database())
    else:
        # Run normal initialization
        asyncio.run(setup_database())
