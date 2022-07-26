from fastapi import APIRouter, status, HTTPException
from passlib.context import CryptContext

from app.schemas import users
from app.crud import users as cu_user

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
    
    return {
        "message": "User Login Success"
    }