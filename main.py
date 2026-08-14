from fastapi import FastAPI, Depends
from models import Base
import models
from database import engine, get_db
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy import select

app = FastAPI()

Base.metadata.create_all(bind=engine)

db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/")
async def home():
    return {"message": "Welcome to project 3"}


# @app.get("/todos/")
# async def real_all(db: db_dependency):
#     return db.query(Todos).all()


@app.get("/todos/")
async def real_all(db: db_dependency):
    result = db.execute(select(models.Todos))
    todos = result.scalars().all()
    return todos
