from typing import Annotated, List
from bson import ObjectId
from fastapi import Depends, HTTPException, Path, Query, APIRouter, status
from fastapi.responses import  JSONResponse
from models.movie_model import Movie
from routes.user_routes import decode_token
from schemas.movie_schema import movie_schema, movies_schema
from db.client import client

movies:List[Movie] = []

movie_router = APIRouter(tags=["movie"],prefix="/movies")

def search_movie(value:dict)-> Movie|dict:
    try:
        found_movie = movie_schema(client.pythontest.movies.find_one(value))
        return found_movie
    except Exception as e:
        return e


@movie_router.post('/', status_code=status.HTTP_201_CREATED)
def post_movie(movie:Movie)-> JSONResponse:
    dic_movie = dict(movie)
    del dic_movie["id"]
    movie_id = client.pythontest.movies.insert_one(dic_movie).inserted_id
    movie = search_movie({"_id":movie_id})
    return JSONResponse(movie,status_code=status.HTTP_201_CREATED)

@movie_router.get('/')
def get_movies()-> JSONResponse:
    movies = movies_schema(client.pythontest.movies.find())
    return JSONResponse(movies,status.HTTP_200_OK)

@movie_router.get('/{id}')
def get_movie(id:str = Path(ge=0)) -> JSONResponse:
    _id = ObjectId(id)
    movie: Movie = search_movie({"_id":_id})
    if not isinstance(movie,Movie):
        raise HTTPException(detail="movie not found",status_code= status.HTTP_400_BAD_REQUEST)
    return JSONResponse(movie,status.HTTP_200_OK)

@movie_router.get('/by_category/{category}')
def get_movie_by_category(category:str)->JSONResponse:
    movie = movies_schema(client.pythontest.movies.find({"category":category}))
    if not isinstance(movie,List):
        raise HTTPException(detail="movie not found",status_code= status.HTTP_400_BAD_REQUEST)
    return JSONResponse(movie,status.HTTP_200_OK)

@movie_router.put('/{id}')
def put_movie(id:str, movie:Movie)-> JSONResponse:
    dic_movie = dict(movie)
    del dic_movie["id"]
    new_movie = movie_schema(client.pythontest.movies.find_one_and_replace(ObjectId(id,dic_movie)))
    return JSONResponse(new_movie,status.HTTP_200_OK)

@movie_router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(id:int):
    for movie in movies:
        if movie.id == id:
            movies.remove(movie)
    return [movie.model_dump() for movie in movies]

@movie_router.get('/video')
def video():
    file_path= "video.mp4"
    return file_path