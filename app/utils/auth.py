from datetime import datetime, timedelta
import jwt
from app.utils.config import settings
from fastapi import HTTPException, status

def generate_jwt(user_id: int) -> str:
    expiry_time = datetime.utcnow() + timedelta(minutes=settings.JWT_TOKEN_TIMEOUT)
    payload = {
        "sub": user_id,
        "exp": expiry_time
    }
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm="HS256")
    return token

def parse_jwt(token: str) -> int:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError as ese:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token Expired")
    except jwt.InvalidSignatureError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Token")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Token")
    except Exception:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Something went wrong")
    return payload["sub"]
        