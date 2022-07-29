from fastapi import status
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from psycopg2.errors import UniqueViolation
from psycopg2.extras import DictCursor
from pydantic import EmailStr

from app.db import conn
from app.schemas.users import BaseUser, RegisterUser

context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create(user: RegisterUser):
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


def get_all(offset: int, limit: int):
    query = "SELECT * FROM library.users OFFSET %s LIMIT %s;"
    params = (offset, limit)
    cursor = conn.cursor(cursor_factory=DictCursor)
    cursor.execute(query, params)
    all_users = cursor.fetchall()
    cursor.close()
    return [dict(user) for user in all_users]


def get_one(id: int):
    query = "SELECT * FROM library.users WHERE id = %s"
    params = (id,)
    cursor = conn.cursor(cursor_factory=DictCursor)
    cursor.execute(query, params)
    user = cursor.fetchone()
    cursor.close()
    return user


def delete(id: int):
    query = "DELETE FROM library.users WHERE id = %s"
    params = (id,)
    cursor = conn.cursor(cursor_factory=DictCursor)
    cursor.execute(query, params)
    conn.commit()
    cursor.close()


def update(user: BaseUser):
    query = """
    UPDATE library.users 
    SET name=%s, 
        email=%s, 
        phone=%s 
    WHERE id=%s RETURNING *;
    """
    params = (user.name, user.email, user.phone, id)
    cursor = conn.cursor(cursor_factory=DictCursor)
    cursor.execute(query, params)
    changed_user_in_db = cursor.fetchone()
    conn.commit()
    cursor.close()
    return changed_user_in_db


def get_by_email(email: EmailStr):
    query = "SELECT * FROM library.users WHERE email = %s"
    params = (email,)
    cursor = conn.cursor(cursor_factory=DictCursor)
    cursor.execute(query, params)
    user = cursor.fetchone()
    cursor.close()
    return user
