import imp
from fastapi import FastAPI

app=FastAPI() 

@app.get("/")
def index():
    return {'data':{'name':'Shivam'}}
 
@app.get('/about')
def about():
    return {'data':'About page'}