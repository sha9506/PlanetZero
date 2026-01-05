from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from bson import ObjectId

from app.models import UserCreate, User, Token
from app.auth import get_password_hash, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app.database import get_database, USERS_COLLECTION

router = APIRouter()

@router.post("/signup", response_model=User, status_code=status.HTTP_201_CREATED)
async def signup(user: UserCreate):
    """Register a new user"""
    db = get_database()
    
    # Check if user already exists
    existing_user = await db[USERS_COLLECTION].find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash password
    hashed_password = get_password_hash(user.password)
    
    # Create user document
    user_dict = user.model_dump(exclude={"password"})
    user_dict.update({
        "hashed_password": hashed_password,
        "points": 0,
        "total_emissions": 0.0,
        "badges": [],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    })
    
    # Insert user
    result = await db[USERS_COLLECTION].insert_one(user_dict)
    
    # Retrieve created user
    created_user = await db[USERS_COLLECTION].find_one({"_id": result.inserted_id})
    created_user["_id"] = str(created_user["_id"])
    
    return User(**created_user)

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login user and return access token"""
    db = get_database()
    
    # Find user by email (username field in OAuth2PasswordRequestForm)
    user = await db[USERS_COLLECTION].find_one({"email": form_data.username})
    
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/consent")
async def accept_consent(email: str):
    """Mark user as having accepted consent"""
    db = get_database()
    
    result = await db[USERS_COLLECTION].update_one(
        {"email": email},
        {"$set": {"consent_accepted": True, "consent_date": datetime.utcnow()}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {"message": "Consent accepted successfully"}
