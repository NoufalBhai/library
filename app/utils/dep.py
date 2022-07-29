from typing import Any

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.utils.auth import parse_jwt


def get_payload(
    token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
) -> dict[str, Any]:
    return parse_jwt(token.credentials)


def get_user(user=Depends(get_payload)):
    if user.get("role") != "USER":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You Don't have Access for perform this operation",
        )
    return user


def get_auth_user(user=Depends(get_payload)):
    if user.get("role") not in ["USER", "Librarian"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You Don't have Access for perform this operation",
        )
    return user


def get_librarian(librarian=Depends(get_payload)):
    if librarian.get("role") != "Librarian":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You Don't have Access for perform this operation",
        )
    return librarian
