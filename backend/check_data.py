"""
Quick script to check MongoDB data
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def check_data():
    client = AsyncIOMotorClient('mongodb://localhost:27017')
    db = client['planetzero_db']
    
    print("\n=== USERS ===")
    users = await db['users'].find().to_list(100)
    for u in users:
        print(f"ID: {u['_id']}, Email: {u['email']}, Name: {u.get('full_name', 'N/A')}")
    
    print("\n=== CARBON FOOTPRINTS ===")
    footprints = await db['carbon_footprints'].find().to_list(100)
    for f in footprints:
        print(f"ID: {f['_id']}, User: {f['user_id']}, Date: {f.get('date')}, Total: {f.get('total_emissions')}kg")
    
    print(f"\nTotal Users: {len(users)}")
    print(f"Total Carbon Footprints: {len(footprints)}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(check_data())
