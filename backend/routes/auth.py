"""
Authentication Routes
Handles user signup, login, and token-based authentication
"""
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from database import get_database, USERS_COLLECTION
from schemas import SignupRequest, LoginRequest, TokenResponse, UserResponse
from services.auth_service import hash_password, verify_password, create_access_token, decode_access_token
from datetime import datetime

router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer()

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(user_data: SignupRequest):
    """
    Register a new user
    
    - Validates email uniqueness
    - Hashes password securely
    - Creates user document in MongoDB
    """
    db = get_database()
    
    # Check if user already exists
    existing_user = await db[USERS_COLLECTION].find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash password
    hashed_password = hash_password(user_data.password)
    
    # Create user document
    user_doc = {
        "email": user_data.email,
        "hashed_password": hashed_password,
        "name": user_data.name,
        "age": user_data.age,
        "gender": user_data.gender,
        "country": user_data.country,
        "city": user_data.city,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "is_active": True
    }
    
    # Insert into database
    result = await db[USERS_COLLECTION].insert_one(user_doc)
    
    # Return user response
    return UserResponse(
        id=str(result.inserted_id),
        email=user_data.email,
        name=user_data.name,
        age=user_data.age,
        gender=user_data.gender,
        country=user_data.country,
        city=user_data.city,
        created_at=user_doc["created_at"],
        is_active=True
    )

@router.post("/login", response_model=TokenResponse)
async def login(credentials: LoginRequest):
    """
    Authenticate user and return JWT token
    
    - Validates email and password
    - Returns access token for subsequent requests
    """
    db = get_database()
    
    print(f"🔍 Login attempt for email: {credentials.email}")
    
    # Find user by email
    user = await db[USERS_COLLECTION].find_one({"email": credentials.email})
    if not user:
        print(f"❌ User not found: {credentials.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    print(f"✅ User found: {user.get('email')}")
    print(f"   Has hashed_password: {'hashed_password' in user}")
    print(f"   Is active: {user.get('is_active')}")
    
    # Verify password
    password_valid = verify_password(credentials.password, user["hashed_password"])
    print(f"   Password valid: {password_valid}")
    
    if not password_valid:
        print(f"❌ Invalid password for: {credentials.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Check if user is active
    if not user.get("is_active", True):
        print(f"❌ Inactive account: {credentials.email}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive"
        )
    
    # Create access token
    access_token = create_access_token(
        data={"sub": str(user["_id"]), "email": user["email"]}
    )
    
    print(f"✅ Login successful for: {credentials.email}")
    return TokenResponse(access_token=access_token, token_type="bearer")

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Dependency to get current authenticated user from JWT token
    
    Used in protected routes to validate user authentication
    """
    token = credentials.credentials
    
    # Decode token
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Get user ID from token
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )
    
    # Fetch user from database
    db = get_database()
    from bson import ObjectId
    user = await db[USERS_COLLECTION].find_one({"_id": ObjectId(user_id)})
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return user
