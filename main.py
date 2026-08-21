from fastapi import FastAPI, Depends, HTTPException, status, Path
from models import Base
import models
from database import engine, get_db
from typing import Annotated

# from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic_models import TodosCreate, TodosResponse, TodosUpdate
from contextlib import asynccontextmanager

# app = FastAPI()

# Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # ShutDown
    await engine.dispose()


app = FastAPI(lifespan=lifespan)


# db_dependency = Annotated[Session, Depends(get_db)]
db_dependency = Annotated[AsyncSession, Depends(get_db)]


@app.get("/", include_in_schema=False)
async def home():
    return {"message": "Welcome to project 3"}


# @app.get("/todos/")
# async def real_all(db: db_dependency):
#     return db.query(Todos).all()


@app.get("/todos/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    result = await db.execute(select(models.Todos))
    todos = result.scalars().all()
    return todos


# It is a strict rule in the Python language: You cannot put a parameter without a default value after a parameter with a default value.
@app.get("/todos/{id}", status_code=status.HTTP_200_OK)
async def get_todo_by_id(db: db_dependency, id: Annotated[int, Path(ge=0)]):
    result = await db.execute(select(models.Todos).where(models.Todos.id == id))
    todo_by_id = result.scalars().first()
    if todo_by_id is not None:
        return todo_by_id
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NO Task Found")


@app.post(
    "/todos/",
    response_model=TodosResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_todo(todo_request: TodosCreate, db: db_dependency):
    todo_dict = todo_request.model_dump()
    new_todo = models.Todos(**todo_dict)
    db.add(new_todo)
    await db.commit()
    await db.refresh(new_todo)
    return new_todo


@app.patch("/todos/{id}", response_model=TodosResponse)
async def update_post(db: db_dependency, id: int, todo_request: TodosUpdate):
    result = await db.execute(select(models.Todos).where(models.Todos.id == id))
    todo = result.scalars().first()
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No Todo of this id present in system",
        )

    todo_dict = todo_request.model_dump(exclude_unset=True)

    for key, value in todo_dict.items():
        setattr(todo, key, value)

    await db.commit()
    await db.refresh(todo)
    return todo


@app.delete("/todos/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, id: Annotated[int, Path(gt=0)]):
    result = await db.execute(select(models.Todos).where(models.Todos.id == id))
    todo = result.scalars().first()
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No todo with such id",
        )
    await db.delete(todo)
    await db.commit()
