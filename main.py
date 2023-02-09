from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse

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

@app.get('/movies', tags=['movies'])
def get_movies():
    return movies

@app.get('/movies/{id}', tags=['movies'])
def get_movie(id:int):
    for item in movies:
        print(item)
        if (item["id"] == id):
            return item 
    return []

@app.get('/movies/', tags=['movies'])
def get_movies_by_category(category: str, year:int):
    return category

@app.get('/movies/category/', tags=['movies'])
def get_movies_by_category(category: str):
    #Mi solucion
    """ for item in movies:
        if (item["category"] == category):
            return item
    return [] """
    # La solucion con una Lambda function
    return [item for item in movies if item["category"] == category]

@app.post('/movies', tags=['movies'])
def create_movie(id: int = Body(), title:str = Body(), overview:str = Body(), year:str = Body(), rating:float = Body(), category:str = Body()):
    movies.append({
        "id":id,
        "title": title,
        "overview": overview,
        "year": year,
        "rating": rating,
        "category": category
    })
    return movies

@app.put('/movies/{id}', tags=['movies'])
def update_movie(id:int, title:str = Body(), overview:str = Body(), year:str = Body(), rating:float = Body(), category:str = Body()):
    for item in movies:
        if item["id"] == id:
            item['title'] = title,
            item['overview'] = overview,
            item['year'] = year,
            item['rating'] = rating,
            item['category'] = category
            return movies

@app.delete('/movies/{id}', tags=['movies'])
def delete_movies(id:int):
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
    return movies