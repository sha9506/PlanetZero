from fastapi import APIRouter, HTTPException, status, Depends
from bson import ObjectId
from typing import List
from datetime import datetime

from app.models import Notification, NotificationCreate, User
from app.auth import get_current_active_user
from app.database import get_database, NOTIFICATIONS_COLLECTION

router = APIRouter()

@router.get("/", response_model=List[Notification])
async def get_notifications(
    current_user: User = Depends(get_current_active_user),
    limit: int = 50,
    unread_only: bool = False
):
    """Get user's notifications"""
    db = get_database()
    
    # Build query
    query = {"user_id": current_user.id}
    if unread_only:
        query["read"] = False
    
    cursor = db[NOTIFICATIONS_COLLECTION].find(query).sort("created_at", -1).limit(limit)
    notifications = await cursor.to_list(length=limit)
    
    for notif in notifications:
        notif["_id"] = str(notif["_id"])
    
    return [Notification(**notif) for notif in notifications]

@router.get("/unread-count")
async def get_unread_count(current_user: User = Depends(get_current_active_user)):
    """Get count of unread notifications"""
    db = get_database()
    
    count = await db[NOTIFICATIONS_COLLECTION].count_documents({
        "user_id": current_user.id,
        "read": False
    })
    
    return {"unread_count": count}

@router.put("/{notification_id}/read")
async def mark_notification_read(
    notification_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Mark a notification as read"""
    db = get_database()
    
    result = await db[NOTIFICATIONS_COLLECTION].update_one(
        {
            "_id": ObjectId(notification_id),
            "user_id": current_user.id
        },
        {"$set": {"read": True}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    
    return {"message": "Notification marked as read"}

@router.put("/read-all")
async def mark_all_read(current_user: User = Depends(get_current_active_user)):
    """Mark all notifications as read"""
    db = get_database()
    
    result = await db[NOTIFICATIONS_COLLECTION].update_many(
        {"user_id": current_user.id, "read": False},
        {"$set": {"read": True}}
    )
    
    return {
        "message": "All notifications marked as read",
        "count": result.modified_count
    }

@router.delete("/{notification_id}")
async def delete_notification(
    notification_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Delete a notification"""
    db = get_database()
    
    result = await db[NOTIFICATIONS_COLLECTION].delete_one({
        "_id": ObjectId(notification_id),
        "user_id": current_user.id
    })
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    
    return {"message": "Notification deleted"}

@router.post("/", response_model=Notification, status_code=status.HTTP_201_CREATED)
async def create_notification(
    notification: NotificationCreate,
    current_user: User = Depends(get_current_active_user)
):
    """Create a new notification (admin/system use)"""
    db = get_database()
    
    notif_dict = notification.model_dump()
    notif_dict.update({
        "read": False,
        "created_at": datetime.utcnow()
    })
    
    result = await db[NOTIFICATIONS_COLLECTION].insert_one(notif_dict)
    
    created_notif = await db[NOTIFICATIONS_COLLECTION].find_one({"_id": result.inserted_id})
    created_notif["_id"] = str(created_notif["_id"])
    
    return Notification(**created_notif)
