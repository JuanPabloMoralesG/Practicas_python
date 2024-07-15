def movie_schema(movie)-> dict:
    return {
            "id":str(movie["_id"]),
            "name": movie["name"],
            "rate": movie["rate"],
            "year": movie["year"],
            "category":movie["category"]
        }
def movies_schema(movies)-> list:
     return [movie_schema(movie) for movie in movies]