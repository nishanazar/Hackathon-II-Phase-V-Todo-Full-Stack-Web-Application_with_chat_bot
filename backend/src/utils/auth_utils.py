from datetime import datetime, timedelta
from typing import Optional
import jwt
from better_abc import settings
from fastapi import HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import os


# Get secret from environment
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "fallback-secret-key-for-development")
ALGORITHM = "HS256"


class TokenData(BaseModel):
    user_id: Optional[str] = None


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a new access token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[TokenData]:
    """
    Verify the JWT token and return the user ID if valid
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
        token_data = TokenData(user_id=user_id)
        return token_data
    except jwt.PyJWTError:
        return None


def get_current_user_id(token: str) -> Optional[str]:
    """
    Get the current user ID from the token
    """
    token_data = verify_token(token)
    if token_data is None:
        return None
    return token_data.user_id


def validate_user_id_from_token(token: str, expected_user_id: str) -> bool:
    """
    Validate that the user ID in the token matches the expected user ID
    This is important for ensuring users can only access their own resources
    """
    token_user_id = get_current_user_id(token)
    if token_user_id is None:
        return False
    return token_user_id == expected_user_id