from . import schemas
from fastapi import FastAPI
from . import models 
from .database import engine
from pydantic import BaseModel
from sqlalchemy.orm import Session

app=FastAPI()
models.Base.metadata.create_all(bind=engine)

@app.post('/blog')
def create(request:schemas.Blog):
    return request
