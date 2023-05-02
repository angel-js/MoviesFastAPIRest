from fastapi import FastAPI, Body, Path, Query, Request, HTTPException, Depends, Response
from fastapi.responses import HTMLResponse, JSONResponse
# Importar Schema
from pydantic import BaseModel, Field
# Optional 
from typing import Optional, List
# JWT 
from utils.jwt_manager import create_token, validate_token
# Middelware
from fastapi.security import HTTPBearer
# Configuracion
from config.database import session, engine, Base
from models.movie import Movie
from models.movie import Movie as MovieModel
# Para mostrar los resultados 
from fastapi.encoders import jsonable_encoder
#middlewares
from middlewares.error_handler import ErrorHandler
#Router
from routers.movie import movie_router
from routers.user import user_router



app = FastAPI()
app.title = "Mi aplicacion con FastAPI"
app.version = "0.0.1"

#Ejecutar un middleware en caso de errores
app.add_middleware(ErrorHandler)
#Utilizar el router
app.include_router(movie_router)
app.include_router(user_router)

Base.metadata.create_all(bind=engine)

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
