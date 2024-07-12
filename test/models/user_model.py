from pydantic import BaseModel, EmailStr

class user(BaseModel):
    id: str | None = None
    username: str
    password: str
    email: EmailStr