from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from models.movie import Movie as MovieModel
from middlewares.jwt_bearer import JWTBearer
from fastapi import Path, Query, Depends
from services.movie import MovieService
from pydantic import BaseModel, Field
from config.database import session
from typing import Optional, List
from models.movie import Movie
from fastapi import APIRouter
from schemas.movie import Movie

movie_router = APIRouter()

@movie_router.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>Hello World</h1>')

@movie_router.get('/movies', tags=['movies'], response_model=List[Movie], dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = session()
    result = MovieService(db).get_movies()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.get('/movies/{id}', tags=['movies'], response_model=Movie)
def get_movie(id: int = Path(ge=1, le=2000,)) -> List[Movie]:
    db = session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={'messagge':'No encontrados'})
    return JSONResponse(status_code=404, content=jsonable_encoder(result))

@movie_router.get('/movies/category/', tags=['movies'], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    db = session()
    result = MovieService(db).get_movie_by_category(category)
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.post('/movies', tags=['movies'], response_model=dict)
def create_movie(movie: Movie) -> dict:
    db = session()
    MovieService(db).create_movie(movie)
    return JSONResponse(status_code=201, content={"message": "Se registro la pelicula"})

@movie_router.put('/movies/{id}', tags=['movies'], response_model=dict)
def update_movie(id:int, movie: Movie)  -> dict:
    db = session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={'messagge':'No encontrado'})
    MovieService(db).update_movie(id, movie)
    db.commit()
    return JSONResponse(status_code=201, content={"message": "Se modifico la pelicula"})

@movie_router.delete('/movies/{id}', tags=['movies'], response_model=dict)
def delete_movies(id:int)  -> dict:
    db = session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'messagge':'No encontrado'})
    return JSONResponse(status_code=201, content={"message": "Se elimino la pelicula"})

