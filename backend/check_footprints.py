"""
Check carbon footprints data
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def check_footprints():
    client = AsyncIOMotorClient('mongodb://localhost:27017')
    db = client['planetzero_db']
    
    print("\n=== CARBON FOOTPRINTS ===")
    footprints = await db['carbon_footprints'].find().to_list(100)
    
    if not footprints:
        print("❌ No carbon footprints found!")
    else:
        print(f"✅ Found {len(footprints)} carbon footprints:")
        for f in footprints:
            print(f"\n  Date: {f.get('date')}")
            print(f"  User ID: {f.get('user_id')}")
            print(f"  Total: {f.get('total_emissions')} kg")
            print(f"  Fields: {list(f.keys())}")
    
    print("\n=== DAILY LOGS ===")
    logs = await db['daily_logs'].find().to_list(100)
    print(f"Found {len(logs)} daily logs:")
    for log in logs:
        print(f"\n  Date: {log.get('date')}")
        print(f"  User ID: {log.get('user_id')}")
        print(f"  Total: {log.get('total_emissions')} kg")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(check_footprints())
