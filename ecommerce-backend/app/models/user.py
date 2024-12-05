from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    id: Optional[str] = None
    email: EmailStr
    password: str  # Password will be provided by the user
    is_admin: bool = False

class UserinDB(BaseModel):
    id: Optional[str] = None
    email: EmailStr
    hashed_password: str
    
class LoginRequest(BaseModel):
    email: str
    password: str