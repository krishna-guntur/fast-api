from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from sqlalchemy.orm import Session

from ToDo_App.database.database import get_db
from ToDo_App.database.database_models import USERS
from .auth import get_current_user
from ToDo_App.config.config import (SECRET_KEY, ALGORITHM, bcrypt_context, oauth2_bearer)

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[Session, Depends(get_current_user)]

@router.get("/get-user")
async def get_user(user: user_dependency, db: db_dependency):

    if user is None:
        raise HTTPException(
            status_code=404,
            detail = "Authentication Failed"
        )
    user_model = db.query(USERS).filter(USERS.id == user.get('user_id')).first()

    if user_model is None:
        raise HTTPException(
            status_code=404,
            detail = "User not found"
        )
    return user_model

@router.get("/change-password")
async def change_password(user: user_dependency,
                          db: db_dependency,
                          new_password):
    
    if user is None:
        return "Authentication Failed"
    user_model = db.query(USERS).filter(USERS.id == user.get("user_id")).first()
    user_model.hashed_password = bcrypt_context.hash(new_password)

    try:
        db.add(user_model)
        db.commit()

        return f"Password changed successfully"
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail= f"An error occurred - {e}"
        )
    


    