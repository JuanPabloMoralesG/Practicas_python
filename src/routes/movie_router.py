from typing import Annotated, List
from fastapi import Depends, Path, Query, APIRouter
from fastapi.responses import FileResponse, JSONResponse
from src.models.movie_model import Movie, movie_create, movie_update
from src.routes.user_routes import decode_token

movies:List[Movie] = []

movie_router = APIRouter()

@movie_router.get('/',tags=["movie"],status_code=200,response_description="la respuesta debe ser exitosa")
def get_movies(my_user:Annotated[dict,Depends(decode_token)])-> JSONResponse:
    return JSONResponse([movie.model_dump() for movie in movies],status_code=200)

@movie_router.get('/{id}',tags=["movie"])
def get_movie(id:int = Path(ge=0)) -> Movie| dict:
    for movie in movies:
        if movie.id == id:
            return JSONResponse(movie.model_dump(),status_code=200)
    return JSONResponse({},status_code=404)

@movie_router.get('/by_category',tags=["movie"])
def get_movie_by_category(category:str =Query(min_length=5,max_length=15))-> Movie| dict:
    for movie in movies:
        if movie.category == category:
            return JSONResponse(movie.model_dump(),status_code=200)
    return JSONResponse({},status_code=404)


@movie_router.post('/',tags=["movie"])
def post_movie(movie:movie_create)-> JSONResponse:
    movies.append(movie)
    return JSONResponse([movie.model_dump() for movie in movies],status_code=201)
    

@movie_router.put('/{id}',tags=["movie"])
def put_movie(id:int, movie:movie_update)-> List[Movie]:
    for item in movies:
        if item.id == id:
            item.name =movie.name
            item.rate=movie.rate
            item.year=movie.year
            item.category=movie.category
    return [movie.model_dump() for movie in movies]

@movie_router.delete('/{id}',tags=["movie"])
def delete_movie(id:int)-> List[Movie]:
    for movie in movies:
        if movie.id == id:
            movies.remove(movie)
    return [movie.model_dump() for movie in movies]

@movie_router.get('/get_file',tags=["movie"])
def get_file():
    return FileResponse('text.txt')