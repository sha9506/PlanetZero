from fastapi import APIRouter, HTTPException, status, Depends
from bson import ObjectId
from typing import List
from datetime import datetime

from app.models import Community, CommunityCreate, CommunityMember, CommunityRole, User
from app.auth import get_current_active_user
from app.database import (
    get_database, 
    COMMUNITIES_COLLECTION, 
    COMMUNITY_MEMBERS_COLLECTION,
    USERS_COLLECTION,
    BADGES_COLLECTION,
    USER_BADGES_COLLECTION,
    NOTIFICATIONS_COLLECTION
)

router = APIRouter()

@router.post("/", response_model=Community, status_code=status.HTTP_201_CREATED)
async def create_community(
    community: CommunityCreate,
    current_user: User = Depends(get_current_active_user)
):
    """Create a new community"""
    db = get_database()
    
    # Create community document
    community_dict = community.model_dump()
    community_dict.update({
        "creator_id": current_user.id,
        "members_count": 1,
        "activities": [],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    })
    
    # Insert community
    result = await db[COMMUNITIES_COLLECTION].insert_one(community_dict)
    community_id = str(result.inserted_id)
    
    # Add creator as community leader
    member_data = {
        "community_id": community_id,
        "user_id": current_user.id,
        "role": CommunityRole.leader,
        "joined_at": datetime.utcnow()
    }
    await db[COMMUNITY_MEMBERS_COLLECTION].insert_one(member_data)
    
    # Award "Community Founder" badge
    founder_badge = await db[BADGES_COLLECTION].find_one({"name": "Community Founder"})
    if founder_badge:
        badge_id = str(founder_badge["_id"])
        
        # Check if user already has this badge
        existing_badge = await db[USER_BADGES_COLLECTION].find_one({
            "user_id": current_user.id,
            "badge_id": badge_id
        })
        
        if not existing_badge:
            # Award badge
            await db[USER_BADGES_COLLECTION].insert_one({
                "user_id": current_user.id,
                "badge_id": badge_id,
                "earned_at": datetime.utcnow()
            })
            
            # Update user's badges array
            await db[USERS_COLLECTION].update_one(
                {"_id": ObjectId(current_user.id)},
                {"$addToSet": {"badges": badge_id}}
            )
            
            # Create notification
            await db[NOTIFICATIONS_COLLECTION].insert_one({
                "user_id": current_user.id,
                "type": "achievement",
                "title": "New Badge Earned!",
                "message": "You earned the Community Founder badge for creating a community!",
                "read": False,
                "created_at": datetime.utcnow()
            })
    
    # Retrieve created community
    created_community = await db[COMMUNITIES_COLLECTION].find_one({"_id": result.inserted_id})
    created_community["_id"] = community_id
    
    return Community(**created_community)

@router.get("/", response_model=List[Community])
async def get_communities(
    category: str = None,
    search: str = None,
    current_user: User = Depends(get_current_active_user)
):
    """Get all communities with optional filters"""
    db = get_database()
    
    # Build query
    query = {}
    if category:
        query["category"] = category
    if search:
        query["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}}
        ]
    
    cursor = db[COMMUNITIES_COLLECTION].find(query).sort("created_at", -1)
    communities = await cursor.to_list(length=None)
    
    for comm in communities:
        comm["_id"] = str(comm["_id"])
    
    return [Community(**comm) for comm in communities]

@router.get("/my-communities", response_model=List[Community])
async def get_my_communities(current_user: User = Depends(get_current_active_user)):
    """Get communities user is a member of"""
    db = get_database()
    
    # Get user's community memberships
    cursor = db[COMMUNITY_MEMBERS_COLLECTION].find({"user_id": current_user.id})
    memberships = await cursor.to_list(length=None)
    
    if not memberships:
        return []
    
    # Get community IDs
    community_ids = [ObjectId(m["community_id"]) for m in memberships]
    
    # Get communities
    cursor = db[COMMUNITIES_COLLECTION].find({"_id": {"$in": community_ids}})
    communities = await cursor.to_list(length=None)
    
    for comm in communities:
        comm["_id"] = str(comm["_id"])
    
    return [Community(**comm) for comm in communities]

@router.get("/{community_id}", response_model=Community)
async def get_community(
    community_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific community"""
    db = get_database()
    
    community = await db[COMMUNITIES_COLLECTION].find_one({"_id": ObjectId(community_id)})
    
    if not community:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Community not found"
        )
    
    community["_id"] = str(community["_id"])
    return Community(**community)

@router.post("/{community_id}/join")
async def join_community(
    community_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Join a community"""
    db = get_database()
    
    # Check if community exists
    community = await db[COMMUNITIES_COLLECTION].find_one({"_id": ObjectId(community_id)})
    if not community:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Community not found"
        )
    
    # Check if already a member
    existing_member = await db[COMMUNITY_MEMBERS_COLLECTION].find_one({
        "community_id": community_id,
        "user_id": current_user.id
    })
    
    if existing_member:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already a member of this community"
        )
    
    # Add member
    member_data = {
        "community_id": community_id,
        "user_id": current_user.id,
        "role": CommunityRole.member,
        "joined_at": datetime.utcnow()
    }
    await db[COMMUNITY_MEMBERS_COLLECTION].insert_one(member_data)
    
    # Update community member count
    await db[COMMUNITIES_COLLECTION].update_one(
        {"_id": ObjectId(community_id)},
        {
            "$inc": {"members_count": 1},
            "$set": {"updated_at": datetime.utcnow()}
        }
    )
    
    # Award points
    await db[USERS_COLLECTION].update_one(
        {"_id": ObjectId(current_user.id)},
        {"$inc": {"points": 25}}
    )
    
    # Create notification
    await db[NOTIFICATIONS_COLLECTION].insert_one({
        "user_id": current_user.id,
        "type": "community",
        "title": "Joined Community!",
        "message": f"You joined {community['name']}",
        "read": False,
        "created_at": datetime.utcnow()
    })
    
    return {"message": "Successfully joined community", "points_awarded": 25}

@router.post("/{community_id}/leave")
async def leave_community(
    community_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Leave a community"""
    db = get_database()
    
    # Check if member
    member = await db[COMMUNITY_MEMBERS_COLLECTION].find_one({
        "community_id": community_id,
        "user_id": current_user.id
    })
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not a member of this community"
        )
    
    # Can't leave if you're the leader
    if member["role"] == CommunityRole.leader:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Community leaders cannot leave. Transfer leadership first."
        )
    
    # Remove member
    await db[COMMUNITY_MEMBERS_COLLECTION].delete_one({
        "community_id": community_id,
        "user_id": current_user.id
    })
    
    # Update community member count
    await db[COMMUNITIES_COLLECTION].update_one(
        {"_id": ObjectId(community_id)},
        {
            "$inc": {"members_count": -1},
            "$set": {"updated_at": datetime.utcnow()}
        }
    )
    
    return {"message": "Successfully left community"}

@router.get("/{community_id}/members")
async def get_community_members(
    community_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get all members of a community"""
    db = get_database()
    
    cursor = db[COMMUNITY_MEMBERS_COLLECTION].find({"community_id": community_id})
    members = await cursor.to_list(length=None)
    
    # Get user details for each member
    member_details = []
    for member in members:
        user = await db[USERS_COLLECTION].find_one({"_id": ObjectId(member["user_id"])})
        if user:
            member_details.append({
                "user_id": member["user_id"],
                "name": user["name"],
                "role": member["role"],
                "joined_at": member["joined_at"]
            })
    
    return member_details

@router.put("/{community_id}/activities")
async def update_community_activities(
    community_id: str,
    activities: List[str],
    current_user: User = Depends(get_current_active_user)
):
    """Update community activities (leaders only)"""
    db = get_database()
    
    # Check if user is a leader
    member = await db[COMMUNITY_MEMBERS_COLLECTION].find_one({
        "community_id": community_id,
        "user_id": current_user.id
    })
    
    if not member or member["role"] != CommunityRole.leader:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only community leaders can update activities"
        )
    
    # Update activities
    await db[COMMUNITIES_COLLECTION].update_one(
        {"_id": ObjectId(community_id)},
        {
            "$set": {
                "activities": activities,
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    return {"message": "Activities updated successfully"}
