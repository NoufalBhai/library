from datetime import datetime, timedelta
from typing import Any

import jwt
from fastapi import HTTPException, status

from app.utils.config import settings


def generate_jwt(user_id: int, role: str) -> str:
    expiry_time = datetime.utcnow() + timedelta(minutes=settings.JWT_TOKEN_TIMEOUT)
    payload = {"sub": user_id, "role": role, "exp": expiry_time}
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm="HS256")
    return token


def parse_jwt(token: str) -> dict[str, Any]:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError as ese:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token Expired"
        )
    except jwt.InvalidSignatureError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Token"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Token"
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Something went wrong"
        )
    return payload
