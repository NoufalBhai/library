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
    conn.commit()
    cursor.close()
    return None

@router.put("/{id}", response_model=schema.ReturnUser)
def update_user(id: int, user: schema.BaseUser):
    query = "SELECT * FROM library.users WHERE id = %s"
    params = (id,)
    cursor = conn.cursor(cursor_factory=DictCursor)
    cursor.execute(query, params)
    user_in_db = cursor.fetchone()
    if not user_in_db:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"message": "No User Found"}
        )

    query = """
    UPDATE library.users 
    SET name=%s, 
        email=%s, 
        phone=%s 
    WHERE id=%s RETURNING *;
    """
    params = (user.name, user.email, user.phone, id)
    
    cursor.execute(query, params)
    changed_user_in_db = cursor.fetchone()
    conn.commit()
    cursor.close()
    return dict(changed_user_in_db)

