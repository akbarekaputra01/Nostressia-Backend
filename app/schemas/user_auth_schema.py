from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional

class UserRegister(BaseModel):
    name: str
    username: str
    email: EmailStr
    password: str
    gender: str
    dob: date
    avatar: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str