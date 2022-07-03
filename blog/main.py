from typing import List
from sqlalchemy import false
from . import schemas
from fastapi import FastAPI,Depends,status,Response,HTTPException
from . import models 
from .database import SessionLocal, engine
from pydantic import BaseModel
from sqlalchemy.orm import Session

from . import hashing

description = """
Blog API helps you do cool stuff. 🚀

## Blogs

You can **Create**, **Read**, **Update** and **Delete** blogs.

## Users

You will be able to:

* **Create users**.
* **Read users**.
"""

app=FastAPI(title="BlogAPI",
    description=description,
    version="0.1.0",)
models.Base.metadata.create_all(bind=engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/blog',status_code=status.HTTP_201_CREATED, tags=['Blogs']) #Create
def create(request:schemas.Blog,db: Session=Depends(get_db)):
    new_blog=models.Blog(title=request.title,body=request.body,user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT,tags=['Blogs']) #Delete
def destroy(id,db: Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with {id} not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return {'done'}

@app.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED,tags=['Blogs']) #Update
def update(id,request:schemas.Blog,db: Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with {id} not found")
    blog.update(request.dict())
    db.commit()
    return 'updated successfully'

    

@app.get('/blog',response_model=List[schemas.ShowBlog],tags=['Blogs']) #Read
def all(db: Session=Depends(get_db)):
    blogs=db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}',status_code=200,response_model=schemas.ShowBlog,tags=['Blogs']) #Read by id
def show(id,response:Response,db: Session=Depends(get_db)):
    blogs=db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    return blogs



@app.post('/user',response_model=schemas.UserOut,tags=['Users'])
def create_user(request:schemas.User,db: Session=Depends(get_db)):
    new_user=models.User(name=request.name,email=request.email,password=hashing.Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/user/{id}',response_model=schemas.UserOut,tags=['Users'])
def get_user(id:int,db: Session=Depends(get_db)):
    users=db.query(models.User).filter(models.User.id==id).first()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    return users