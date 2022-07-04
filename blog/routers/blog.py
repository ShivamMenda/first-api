from fastapi import APIRouter,Depends,status,HTTPException,Response
from .. import schemas,models
from typing import List
from .. import database
from sqlalchemy.orm import Session
get_db=database.get_db
router=APIRouter(
    prefix="/blog",
    tags=["Blogs"]
)

@router.get('/',response_model=List[schemas.ShowBlog]) #Read
def all(db: Session=Depends(database.get_db)):
    blogs=db.query(models.Blog).all()
    return blogs

@router.post('/',status_code=status.HTTP_201_CREATED) #Create
def create(request:schemas.Blog,db: Session=Depends(get_db)):
    new_blog=models.Blog(title=request.title,body=request.body,user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT) #Delete
def destroy(id,db: Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with {id} not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return {'done'}

@router.put('/{id}',status_code=status.HTTP_202_ACCEPTED) #Update
def update(id,request:schemas.Blog,db: Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with {id} not found")
    blog.update(request.dict())
    db.commit()
    return 'updated successfully'

@router.get('/{id}',status_code=200,response_model=schemas.ShowBlog) #Read by id
def show(id,db: Session=Depends(get_db)):
    blogs=db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    return blogs