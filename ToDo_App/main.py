from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from starlette import status

from database import engine, local_session
import models
from models import TODOS
from todoRequest import TodoRequest


app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = local_session()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/get_todos")
def get_all_todos(db: db_dependency):
    return db.query(TODOS).all()

@app.get("/get_todos/{todo_id}", status_code=status.HTTP_200_OK)
async def get_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(TODOS).filter(TODOS.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise  HTTPException(
        status_code=404,
        detail=f"Record with ID {todo_id} not found"
    )

@app.post("/create_todo", status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, new_todo: TodoRequest):
    todo_model = TODOS(
        **new_todo.model_dump()
    )
    db.add(todo_model)
    db.commit()