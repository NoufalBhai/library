
from fastapi import APIRouter, HTTPException, Response, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
from psycopg2.extras import DictCursor

from app import schema
from app.db import conn

router = APIRouter()

@router.post("/", response_model=schema.ReturnUser)
def add_user(user: schema.RegisterUser):
    query = """
    INSERT INTO library.users(name, phone, email, password)
    VALUES (%s, %s, %s, %s) RETURNING *;
    """
    params = (user.name, user.phone, user.email, user.password)
    cursor = conn.cursor(cursor_factory=DictCursor)
    cursor.execute(query, params)
    conn.commit()
    new_user = cursor.fetchone()
    
    return dict(new_user)


fake_database = {
    1: {
        "id": 1,
        "name": "User 1",
        "email": "user1@email.com"
    },
    2: {
        "id": 2,
        "name": "User 2",
        "email": "user2@email.com"
    },
    3: {
        "id": 3,
        "name": "User 3",
        "email": "user3@email.com"
    },
    4: {
        "id": 4,
        "name": "User 4",
        "email": "user4@email.com"
    },
    5: {
        "id": 5,
        "name": "User 5",
        "email": "user5@email.com"
    },
    6: {
        "id": 6,
        "name": "User 6",
        "email": "user6@email.com"
    }
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



@router.get("/", response_model=list[ReturnUser])
def get_all_users(limit: int=3, offset: int=0):
    return list(fake_database.values())[offset: offset+limit]

@router.get("/{id}", response_model=ReturnUser, responses={
    200: {"model": RegisterUser},
    404: {"model": dict[str, str]}
})
def get_user(id: int):
    try:
        user = fake_database[id]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")
    return user

@router.put("/{id}", response_model=ReturnUser)
def update_user(id: int, change_user: UpdateUser):
    try:
        user = fake_database[id]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")
    
    user.update(change_user.dict())
    fake_database[id] = user
    
    return user

@router.delete("/{id}", status_code=204, response_class=Response)
def delete_user(id: int):
    try:
        user = fake_database[id]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")
    del fake_database[id]
    return None