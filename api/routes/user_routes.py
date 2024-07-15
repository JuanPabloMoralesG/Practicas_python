
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt 
from models.user_model import user
from fastapi.responses import JSONResponse
from decouple import config
from db.client import client
from schemas.user_schema import user_schema, users_schema



user_routes = APIRouter(tags=["user"])
oauth2_squema = OAuth2PasswordBearer(tokenUrl="token")
key = config("ENCRYPTION_KEY")
algorithm="HS256"

def encode_password(raw_password: dict) -> str:
    return jwt.encode(raw_password,key,algorithm)

def decode_password(hashe_password:str) ->dict:
    return jwt.decode(hashe_password,key,algorithms=[algorithm])

def encode_token(payload:dict)-> str:
    return jwt.encode(payload,key,algorithm)

def decode_token(token:Annotated[str,Depends(oauth2_squema)])-> dict:
    data = jwt.decode(token,key,algorithms=["HS256"])
    user = search_user_by_data({"username":data["username"]})
    return user

def search_user_by_data(value:dict)-> user|dict:
    try:
        found_user = user_schema(client.pythontest.users.find_one(value))
        print(found_user)
        return user(**found_user)
    except Exception as e:
        return e

@user_routes.post("/user/sing-up", response_model=user,status_code=status.HTTP_201_CREATED)
async def create_user(new_user: user) -> JSONResponse:
    user_dict = dict(new_user)
    del user_dict["id"]
    user_dict["password"] = encode_password({"password":user_dict["password"]})
    if type(search_user_by_data({"email":user_dict["email"]}))==user:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,detail="There is a user registered with this email")
    
    _id = client.pythontest.users.insert_one(user_dict).inserted_id
    inserted_user = user_schema(client.pythontest.users.find_one({"_id":_id}))

    return JSONResponse(inserted_user,status.HTTP_201_CREATED)

@user_routes.post("/token")
def login(form_data:Annotated[OAuth2PasswordRequestForm, Depends()]):
    loging_user = search_user_by_data({"username":form_data.username})
    password= decode_password(loging_user.password)
    if type(loging_user) != user or form_data.password != password["password"]: 
        raise HTTPException(status_code=400,detail="incorrect username or password")
    
    token = encode_token({"username":loging_user.username,"email":loging_user.email})
    return {"access_token":token}

@user_routes.put("/user",status_code=status.HTTP_200_OK)
def update(my_user:Annotated[dict,Depends(decode_token)], new_user:user):
    user_dict:dict = dict(new_user)
    del user_dict["id"]
    user_dict["password"] = encode_password({"password":user_dict["password"]})
    try:
        client.pythontest.users.find_one_and_replace({"email":my_user.email},user_dict)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=e)

    return search_user_by_data({"email":my_user.email})

@user_routes.get("/user/profile")
def profile(my_user:Annotated[dict,Depends(decode_token)]):
    my_user.password = decode_password(my_user.password)["password"]
    return my_user


class commons_dep():
    def __init__(self,start_date,end_date) -> None:
        self.start_date = start_date
        self.end_date= end_date

@user_routes.get("/users")
def get_users(): 
    users = users_schema(client.pythontest.users.find())
    return JSONResponse(users,status.HTTP_200_OK)

@user_routes.delete("/users/{email}",status_code=status.HTTP_204_NO_CONTENT)
def delete_user(my_user:Annotated[dict,Depends(decode_token)],email:str):

    if type(search_user_by_data({"email":email})) != user:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,detail="There is not a user registered with this email")
    client.pythontest.users.find_one_and_delete({"email":email})
    return JSONResponse(status.HTTP_204_NO_CONTENT)