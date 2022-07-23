from pydantic import BaseModel, EmailStr


class UserID(BaseModel):
    id: int


class BaseUser(BaseModel):
    name: str
    email: EmailStr
    phone: str


class ReturnUser(BaseUser, UserID):
    pass


class RegisterUser(BaseUser):
    password: str
