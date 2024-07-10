from pydantic import BaseModel, EmailStr

class user_in(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None

class user_out(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None

class user_indb(BaseModel):
    username: str
    hashed_password: str
    email: EmailStr
    full_name: str | None = None

