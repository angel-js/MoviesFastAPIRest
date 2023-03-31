from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
# Importar Schema
from pydantic import BaseModel, Field
# Optional 
from typing import Optional, List

class Movie(BaseModel):
    id: Optional[int] = None
    title : str = Field(min_length=5, max_length=15)
    overview : str = Field( min_length=15, max_length=50)
    year : int = Field(le=2023)
    rating : float = Field(ge=1, le=10.0)
    category : str = Field(min_length=3, max_length=25)

    class Config:
        schema_extra = {
            "example": {
            "id":1,
            "title": "Mi película",
            "overview": "Descripcion de la pelicula",
            "year": 2022,
            "rating" :5.0,
            "category": "Acción",      
            }
        }

movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'    
    },
    {
        'id': 2,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'    
    },
    {
        'id': 3,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'    
    }   
]

app = FastAPI()
app.title = "Mi aplicacion con FastAPI"
app.version = "0.0.1"

@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>Hello World</h1>')

@app.get('/movies', tags=['movies'], response_model=List[Movie])
def get_movies() -> List[Movie]:
    return JSONResponse(status_code=200, content=movies)

@app.get('/movies/{id}', tags=['movies'], response_model=Movie)
def get_movie(id: int = Path(ge=1, le=2000,)) -> List[Movie]:
    for item in movies:
        print(item)
        if (item["id"] == id):
            return JSONResponse(status_code=200, content=item)
    return JSONResponse(status_code=404, content=[])

@app.get('/movies/category/', tags=['movies'], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    #Mi solucion
    """ for item in movies:
        if (item["category"] == category):
            return item
    return [] """
    # La solucion con una Lambda function
    data = [item for item in movies if item["category"] == category]
    return JSONResponse(status_code=200, content=data)

@app.post('/movies', tags=['movies'], response_model=dict)
def create_movie(movie: Movie) -> dict:
    movies.append(movie)
    return JSONResponse(status_code=201, content={"message": "Se registro la pelicula"})

@app.put('/movies/{id}', tags=['movies'], response_model=dict)
def update_movie(id:int, movie: Movie)  -> dict:
    for item in movies:
        if item["id"] == id:
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category
            return JSONResponse(status_code=201, content={"message": "Se modifico la pelicula"})

@app.delete('/movies/{id}', tags=['movies'], response_model=dict)
def delete_movies(id:int)  -> dict:
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
    return JSONResponse(status_code=201, content={"message": "Se elimino la pelicula"})