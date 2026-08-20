from fastapi import FastAPI, Depends, HTTPException, status, Path
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


@app.get("/todos/", status_code=status.HTTP_200_OK)
async def real_all(db: db_dependency):
    result = db.execute(select(models.Todos))
    todos = result.scalars().all()
    return todos


# It is a strict rule in the Python language: You cannot put a parameter without a default value after a parameter with a default value.
@app.get("/todos/get_todo/{id}", status_code=status.HTTP_200_OK)
async def get_todo_by_id(db: db_dependency, id: Annotated[int, Path(ge=0)]):
    result = db.execute(select(models.Todos).where(models.Todos.id == id))
    todo_by_id = result.scalars().first()
    if todo_by_id is not None:
        return todo_by_id
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NO Task Found")
