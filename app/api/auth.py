from fastapi import APIRouter, Depends, Request, status, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext

from app.schemas import users
from app.crud import users as cu_user
from app.utils.auth import generate_jwt, parse_jwt

router = APIRouter()

context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/login")
def login(user: users.Login):
    user_in_db = cu_user.get_by_email(user.email)
    if not user_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found"
        )
    password_in_db = user_in_db.get("password")
    if not context.verify(user.password, password_in_db):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email or Password Missmatch"
        )
    token = generate_jwt(user_in_db.get("id"))
    return {
        "message": "User Login Success",
        "access_token": token
    }

def get_user_id(token: HTTPAuthorizationCredentials=Depends(HTTPBearer())) -> str:
    return parse_jwt(token.credentials)

@router.get("/only-for-logged-in")
def secret_data(user_id: int = Depends(get_user_id)):
    return {
        "message": "It's only for logged in Users",
        "data": "This is a secret",
        "user_id": user_id 
    }

