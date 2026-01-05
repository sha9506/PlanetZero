"""
Test login credentials
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def test_login():
    client = AsyncIOMotorClient('mongodb://localhost:27017')
    db = client['planetzero_db']
    
    email = "ravi.kumar@example.com"
    password = "Password123"
    
    # Find user
    user = await db['users'].find_one({'email': email})
    
    if not user:
        print(f"❌ User not found: {email}")
        return
    
    print(f"✅ User found: {user['email']}")
    print(f"   Name: {user.get('name')}")
    print(f"   ID: {user['_id']}")
    print(f"   Password Hash: {user.get('password_hash')[:50]}...")
    
    # Verify password
    if pwd_context.verify(password, user['password_hash']):
        print(f"✅ Password verified successfully!")
    else:
        print(f"❌ Password verification failed!")
        print(f"   Trying to hash '{password}'...")
        new_hash = pwd_context.hash(password)
        print(f"   New hash: {new_hash}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(test_login())
