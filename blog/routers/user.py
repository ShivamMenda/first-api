from fastapi import APIRouter,Depends,status,HTTPException,Response
from .. import schemas,models
from typing import List
from .. import database
from sqlalchemy.orm import Session
from .. import hashing
get_db=database.get_db
router=APIRouter(
    prefix="/user",
    tags=["Users"]
)

@router.get('/',response_model=List[schemas.UserOut]) #Read all
def all(db: Session=Depends(get_db)):
    users=db.query(models.User).all()
    return users

@router.post('/',response_model=schemas.UserOut)
def create_user(request:schemas.User,db: Session=Depends(get_db)):
    new_user=models.User(name=request.name,email=request.email,password=hashing.Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/{id}',response_model=schemas.UserOut)
def get_user(id:int,db: Session=Depends(get_db)):
    users=db.query(models.User).filter(models.User.id==id).first()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    return users

# @router.delete('/user/{id}',status_code=status.HTTP_204_NO_CONTENT)
# def delete_user(id,db: Session=Depends(get_db)):
#     user=db.query(models.User).filter(models.User.id==id)
#     if not user.first():
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id {id} not found")
#     user.delete(synchronize_session=False)
#     db.commit()
#     return {'done'}

# @router.put('/user/{id}',status_code=status.HTTP_202_ACCEPTED)
# def update(id,request:schemas.UserUpdate,db: Session=Depends(get_db)):
#     user=db.query(models.User).filter(models.User.id==id)
#     if not user.first():
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id {id} not found")
#     user.update(request.dict())
#     db.commit()
#     return 'updated successfully'