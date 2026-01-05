"""
Debug login issue
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def debug_login():
    client = AsyncIOMotorClient('mongodb://localhost:27017')
    db = client['planetzero_db']
    
    email = "ravi.kumar@example.com"
    password = "Password123"
    
    # Find user
    user = await db['users'].find_one({'email': email})
    
    if not user:
        print(f"❌ User not found with email: {email}")
        print("\nAll users in database:")
        all_users = await db['users'].find().to_list(100)
        for u in all_users:
            print(f"  - {u.get('email')} | Fields: {list(u.keys())}")
        client.close()
        return
    
    print(f"✅ User found!")
    print(f"   Email: {user.get('email')}")
    print(f"   Name: {user.get('name')}")
    print(f"   Is Active: {user.get('is_active')}")
    print(f"   Fields: {list(user.keys())}")
    
    # Check for password field
    if 'hashed_password' in user:
        print(f"   ✅ Has 'hashed_password' field")
        print(f"   Hash: {user['hashed_password'][:60]}...")
        
        # Test password verification
        try:
            is_valid = pwd_context.verify(password, user['hashed_password'])
            if is_valid:
                print(f"   ✅ Password '{password}' is VALID!")
            else:
                print(f"   ❌ Password '{password}' is INVALID!")
        except Exception as e:
            print(f"   ❌ Error verifying password: {e}")
    elif 'password_hash' in user:
        print(f"   ❌ Has 'password_hash' field (should be 'hashed_password')")
        print(f"   Hash: {user['password_hash'][:60]}...")
    else:
        print(f"   ❌ No password field found!")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(debug_login())
