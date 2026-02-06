from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
import os
from functools import wraps

# Using the same authentication approach as the existing system
security = HTTPBearer()

# Get secret key from environment - fallback to default for development
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a new access token with the provided data
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str):
    """
    Verify the provided token and return the payload
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user_id
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Get the current user from the token in the Authorization header
    Returns the user_id from the token
    """
    token = credentials.credentials
    user_id = verify_token(token)
    return user_id


def verify_user_id_match(current_user_id: str, path_user_id: str):
    """
    Verify that the user_id in the JWT matches the user_id in the path
    Raises HTTPException if they don't match
    """
    if current_user_id != path_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User ID in token does not match user ID in request"
        )


def require_same_user_or_admin(current_user_id: str, resource_user_id: str):
    """
    Verify that the current user is the same as the resource owner or is an admin
    """
    # For now, just check if the user IDs match
    # In the future, we could add admin role checking
    if current_user_id != resource_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this resource"
        )