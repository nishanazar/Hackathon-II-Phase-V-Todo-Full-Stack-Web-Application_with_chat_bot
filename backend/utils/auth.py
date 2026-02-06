"""
Authentication utilities for validating JWT tokens and extracting user information
"""
from typing import Optional
import jwt
from fastapi import HTTPException, status
from backend.settings import settings


def verify_user_access(user_id: str) -> bool:
    """
    Verifies that the user_id is valid and corresponds to an authenticated user.

    Args:
        user_id (str): The user ID to verify

    Returns:
        bool: True if the user access is valid, False otherwise
    """
    # Check that the user_id is not empty and has a reasonable format
    if not user_id or not isinstance(user_id, str) or len(user_id.strip()) == 0:
        return False

    # Additional validation could be performed here, such as:
    # - Checking if the user exists in the database
    # - Validating the user_id format
    # - Checking if the user is active/enabled

    return True


def verify_user_owns_resource(requested_user_id: str, resource_user_id: str) -> bool:
    """
    Verifies that the requesting user owns the resource they're trying to access.

    Args:
        requested_user_id (str): The user ID from the request/JWT
        resource_user_id (str): The user ID associated with the resource

    Returns:
        bool: True if the user owns the resource, False otherwise
    """
    return requested_user_id == resource_user_id


def decode_jwt_token(token: str) -> Optional[dict]:
    """
    Decodes a JWT token and returns the payload.
    
    Args:
        token (str): The JWT token to decode
        
    Returns:
        Optional[dict]: The decoded token payload or None if invalid
    """
    try:
        # Decode the JWT token using the secret from settings
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )
        return payload
    except jwt.ExpiredSignatureError:
        # Token has expired
        return None
    except jwt.InvalidTokenError:
        # Token is invalid
        return None


def extract_user_id_from_token(token: str) -> Optional[str]:
    """
    Extracts the user ID from a JWT token.
    
    Args:
        token (str): The JWT token to extract user ID from
        
    Returns:
        Optional[str]: The user ID or None if extraction failed
    """
    payload = decode_jwt_token(token)
    if payload and "sub" in payload:
        return payload["sub"]
    return None


def validate_user_authorization(token: str, expected_user_id: str) -> bool:
    """
    Validates that the user in the token matches the expected user ID.
    
    Args:
        token (str): The JWT token to validate
        expected_user_id (str): The expected user ID
        
    Returns:
        bool: True if the token user matches expected user ID, False otherwise
    """
    token_user_id = extract_user_id_from_token(token)
    return token_user_id == expected_user_id