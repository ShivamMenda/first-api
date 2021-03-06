from cgitb import text
import imp
from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel
import uvicorn

app=FastAPI() 
#To access docs add /docs to access Swagger UI

@app.get("/blog")
def index(limit=10,published:bool=True,sort: Optional[str]= None): #Passing default values and optional values(Query params)
    if(published==True):
        return {'data':f'{limit} published blogs from db'}
    else:
        return {'data':f'{limit} blogs from db'}

@app.get('/blog/unpublished')  #Static needs to be above dynamic as its line by line reading
def unpublished():
    return{'data':'unpublished blogs'}
 
@app.get('/blog/{id}')
def show(id: int): #Type matching with Pydantic under the hood.
    return {'data':id}


@app.get('/blog/{id}/comments') #Path params
def comment(id):
    return {'data':{'1','2'}}

class Blog(BaseModel): #BaseModel 
    title:str
    body:str
    published:Optional[bool]


@app.post('/blog') #post request with pydantic model
def create_blog(request:Blog):
    return{'data':f"Blog is created with title {request.title}"}


# if __name__=="__main__":  #To change ports
#     uvicorn.run(app,host="127.0.0.1",port=5500)