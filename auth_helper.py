from fastapi import HTTPException
from models import User, UserTier
from database import Session
import secrets
from datetime import datetime, timedelta

def generate_api_key():
    return secrets.token_urlsafe(32)

def check_tier_access(user: User, required_tier: UserTier):
    tier_priority = {
        UserTier.FREE: 1,
        UserTier.PRO: 2,
        UserTier.ENTERPRISE: 3
    }
    
    if tier_priority[user.tier] < tier_priority[required_tier]:
        raise HTTPException(
            status_code=403,
            detail=f"This feature requires {required_tier.value} tier. Please upgrade."
        )
    return True

def get_user_by_api_key(api_key: str):
    db = Session()
    user = db.query(User).filter(User.api_key == api_key).first()
    db.close()
    return user