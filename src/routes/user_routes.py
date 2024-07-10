
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt 
users = {
    "juan":{"username":"juan","password":"12345","email":"email@email.com"},
    "pablo":{"username":"pablo","password":"12345","email":"email2@email.com"}
}

user_routes = APIRouter()
oauth2_squema = OAuth2PasswordBearer(tokenUrl="token")

def encode_token(payload:dict)-> str:
    return jwt.encode(payload,"my-secret",algorithm="HS256")


def decode_token(token:Annotated[str,Depends(oauth2_squema)])-> dict:
    data = jwt.decode(token,"my-secret",algorithms=["HS256"])
    user = users.get(data["username"])
    return user


@user_routes.post("/token",tags=["users"])
def login(form_data:Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = users.get(form_data.username)
    if not user or form_data.password != user["password"]: 
        raise HTTPException(status_code=400,detail="incorrect username or password")
    token = encode_token({"username":user["username"],"email":user["email"]})
    return {"access_token":token}

@user_routes.get("/user/profile", tags=["users"])
def profile(my_user:Annotated[dict,Depends(decode_token)]):
    return my_user


class commons_dep():
    def __init__(self,start_date,end_date) -> None:
        self.start_date = start_date
        self.end_date= end_date


@user_routes.get("/", tags=["users"])
def get_users(commons:commons_dep = Depends(commons_dep)):
    return f"users created between {commons.start_date} and {commons.end_date}"


