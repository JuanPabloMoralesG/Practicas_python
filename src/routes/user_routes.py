
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt 
from src.models.user_model import user_in,user_out,user_indb
from fastapi.responses import JSONResponse
from decouple import config
users = {"juan":{"username":"juan","password":"12345","email":"example@example.com"}}
users_out= {"juan":{"username":"juan","password":"12345","email":"example@example.com"}}

user_routes = APIRouter()
oauth2_squema = OAuth2PasswordBearer(tokenUrl="token")

def encode_token(payload:dict)-> str:
    key = config("ENCRYPTION_KEY")
    return jwt.encode(payload,key,algorithm="HS256")

def password_hasher(raw_password: str):
    return "supersecret" + raw_password

def decode_token(token:Annotated[str,Depends(oauth2_squema)])-> dict:
    data = jwt.decode(token,config("ENCRYPTION_KEY"),algorithms=["HS256"])
    user = users.get(data["username"])
    return user

@user_routes.post("/token",tags=["users"])
def login(form_data:Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = users_out.get(form_data.username)
    if not user or form_data.password != user["password"]: 
        raise HTTPException(status_code=400,detail="incorrect username or password")
    token = encode_token({"username":user["username"],"email":user["email"]})
    return {"access_token":token}

@user_routes.post("/user/singup", response_model=user_in,tags=["users"])
async def create_user(user_in: user_in) -> JSONResponse:
    users[user_in.username] = {"username":user_in.username,"password":user_in.password,"email":user_in.email}
    return JSONResponse(users,status.HTTP_201_CREATED)


@user_routes.get("/user/profile", tags=["users"])
def profile(my_user:Annotated[dict,Depends(decode_token)]):
    return my_user


class commons_dep():
    def __init__(self,start_date,end_date) -> None:
        self.start_date = start_date
        self.end_date= end_date

@user_routes.get("/users", tags=["users"])
def get_users(my_user:Annotated[dict,Depends(decode_token)]):
    return JSONResponse(users,status.HTTP_200_OK)


