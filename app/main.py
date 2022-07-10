from fastapi import FastAPI
from blog import models 
from blog.database import engine
from blog.routers import blog,user,authentication

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

app.include_router(authentication.router)
app.include_router(blog.router)
app.include_router(user.router)