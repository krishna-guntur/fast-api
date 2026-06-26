from fastapi import APIRouter, Depends, Path, HTTPException
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status

from models import TODOS
from database import local_session
from todoRequest import TodoRequest
from .auth import get_current_user


router = APIRouter()

def get_db():
    db = local_session()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/get_todos")
def get_all_todos(user: user_dependency, db: db_dependency):
    if user is None:
        return "Authentication Failed"
    
    try:
        print(f"user.id = {user.get('id')}")
        print(f"user.name = {user.get('name')}")
        return db.query(TODOS).filter(TODOS.owner_id == user.get('user_id')).all()
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail="Not found"
        )


@router.get("/get_todos/{todo_id}", status_code=status.HTTP_200_OK)
async def get_todo(user: user_dependency,
                   db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    todo_model = db.query(TODOS).filter(TODOS.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise  HTTPException(
        status_code=404,
        detail=f"Record with ID {todo_id} not found"
    )

@router.post("/create_todo", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency,
                      db: db_dependency, new_todo: TodoRequest):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    todo_model = TODOS(
        **new_todo.model_dump(),
        owner_id= user.get('user_id')
    )
    db.add(todo_model)
    db.commit()

@router.put("/update_todo", status_code=status.HTTP_202_ACCEPTED)
async def update_todo(user: user_dependency, 
                      db: db_dependency, update_to: TodoRequest, todo_id: int):
    
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed.")
    todo_model = db.query(TODOS).filter(TODOS.id == todo_id).first()
    todo_model.title = update_to.title
    todo_model.description = update_to.description
    todo_model.priority = update_to.priority
    todo_model.complete = update_to.complete

    db.add(todo_model)
    db.commit()

@router.delete("/delete_todo", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency,
                      db: db_dependency, todo_id: int):
    
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed.")
    todos_model = db.query(TODOS).filter(TODOS.id == todo_id).first()
    db.delete(todos_model)
    db.commit()