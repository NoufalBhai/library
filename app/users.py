from fastapi import APIRouter, HTTPException, Response, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
from psycopg2.extras import DictCursor
from psycopg2.errors import UniqueViolation

from passlib.context import CryptContext

from app import schema
from app.db import conn

router = APIRouter()

context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/", response_model=schema.ReturnUser)
def add_user(user: schema.RegisterUser):
    """
    This Function Will Create a new user
    """
    query = """
    INSERT INTO library.users(name, phone, email, password)
    VALUES (%s, %s, %s, %s) RETURNING *;
    """
    hashed_pwd = context.hash(user.password)
    params = (user.name, user.phone, user.email, hashed_pwd)
    try:
        cursor = conn.cursor(cursor_factory=DictCursor)
        cursor.execute(query, params)
        conn.commit()
        new_user = cursor.fetchone()
    except UniqueViolation as uv:
        conn.rollback()
        if "users_email_key" in str(uv):
            message = "Email is already Exist"
        if "users_phone_key" in str(uv):
            message = "Phone number is already Exist"
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"message": message}
        )
    finally:
        cursor.close()
    return dict(new_user)


@router.get("/", response_model=list[schema.ReturnUser])
def get_all_users(limit: int = 3, offset: int = 0):
    query = "SELECT * FROM library.users OFFSET %s LIMIT %s;"
    params = (offset, limit)
    cursor = conn.cursor(cursor_factory=DictCursor)
    cursor.execute(query, params)
    all_users = cursor.fetchall()
    cursor.close()
    # au = []
    # for user in all_users:
    #     au.append(dict(user))
    return [dict(user) for user in all_users]


@router.get(
    "/{id}",
    response_model=schema.ReturnUser,
    responses={200: {"model": schema.RegisterUser}, 404: {"model": dict[str, str]}},
)
def get_user(id: int):
    query = "SELECT * FROM library.users WHERE id = %s"
    params = (id,)
    cursor = conn.cursor(cursor_factory=DictCursor)
    cursor.execute(query, params)
    user = cursor.fetchone()
    cursor.close()
    if not user:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"message": "No User Found"}
        )

    return dict(user)

@router.delete("/{id}", status_code=204, response_class=Response)
def delete_user(id: int):
    query = "SELECT * FROM library.users WHERE id = %s"
    params = (id,)
    cursor = conn.cursor(cursor_factory=DictCursor)
    cursor.execute(query, params)
    user = cursor.fetchone()
    cursor.close()
    if not user:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"message": "No User Found"}
        )
    
    query = "DELETE FROM library.users WHERE id = %s"
    params = (id,)
    cursor = conn.cursor(cursor_factory=DictCursor)
    cursor.execute(query, params)
    cursor.close()
    return None


fake_database = {
    1: {"id": 1, "name": "User 1", "email": "user1@email.com"},
    2: {"id": 2, "name": "User 2", "email": "user2@email.com"},
    3: {"id": 3, "name": "User 3", "email": "user3@email.com"},
    4: {"id": 4, "name": "User 4", "email": "user4@email.com"},
    5: {"id": 5, "name": "User 5", "email": "user5@email.com"},
    6: {"id": 6, "name": "User 6", "email": "user6@email.com"},
}


class UserID(BaseModel):
    id: int


class BaseUser(BaseModel):
    name: str
    email: EmailStr


class RegisterUser(BaseUser):
    pass


class UpdateUser(BaseUser):
    pass


class ReturnUser(BaseUser, UserID):
    pass


@router.put("/{id}", response_model=ReturnUser)
def update_user(id: int, change_user: UpdateUser):
    try:
        user = fake_database[id]
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found"
        )

    user.update(change_user.dict())
    fake_database[id] = user

    return user
