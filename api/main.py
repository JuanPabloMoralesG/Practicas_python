from fastapi import FastAPI, Depends, Form
from fastapi.requests import Request
from routes.movie_router import movie_router
from routes.user_routes import user_routes
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from utils.http_error_handler import http_error_handler

static_path = os.path.join(os.path.dirname(__file__),"static/")
templates_path = os.path.join(os.path.dirname(__file__),"templates/")


app = FastAPI()
app.title = "Nueva App"
app.version = "1.0"
app.add_middleware(http_error_handler)
app.mount("/static",StaticFiles(directory=static_path),"static")
templates = Jinja2Templates(directory=templates_path)




@app.get('/',tags=["home"])
def home(request:Request):
   return templates.TemplateResponse("index.html",{"request":request,"message":"Welcome"})

app.include_router(router=user_routes)
app.include_router(router=movie_router)
