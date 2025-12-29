from fastapi import Depends, HTTPException, status
from .auth import get_current_user       # 'app.utils.auth' yerine '.auth'
from .models import User                # 'app.models' yerine '.models'

def admin_required(current_user: User = Depends(get_current_user)):
    # Not: User modelinde 'is_admin' alanı yoksa 'role == "admin"' kullanmalısın
    if current_user.role != "admin": 
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admins only"
        )
    return current_user