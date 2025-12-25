from fastapi import Depends, HTTPException, status
from app.utils.auth import get_current_user
from app.models import User

def admin_required(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admins only"
        )
    return current_user
