from fastapi import FastAPI
from fastapi.responses import  PlainTextResponse
from src.routes.movie_router import movie_router


app = FastAPI()

app.title = "Nueva App"
app.version = "1.0"


@app.get('/',tags=["home"])
def home():
    return PlainTextResponse("Hello world", status_code=200)

app.include_router(prefix="/movies",router=movie_router)
