from fastapi import Depends, HTTPException, status
from app.core.auth import get_current_user
from app.schemas.user_schema import UserResponse

def role_required(role: str):
    """
    This is a dependency to check if the user has the required role.
    It raises an HTTPException if the user's role does not match.
    """
    def _role_required(user: UserResponse = Depends(get_current_user)):
        if user.role != role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User does not have the required {role} role."
            )
        return user
    
    return _role_required
