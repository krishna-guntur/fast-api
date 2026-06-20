from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.testing.plugin.plugin_base import post
from starlette import status

from passlib.context import CryptContext

from database import local_session
from routers.users import CreateUser
from models import USERS
router = APIRouter()

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def get_db():
    db = local_session()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

def authenticate_user(username:str, password:str, db: db_dependency):
    user = db.query(USERS).filter(USERS.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return True


@router.post("/create-user", status_code=status.HTTP_201_CREATED)
async def get_user(db: db_dependency, user_request: CreateUser):
    create_user_model = USERS(
        email = user_request.email,
        username = user_request.username,
        first_name = user_request.first_name,
        last_name = user_request.last_name,
        role = user_request.role,
        hashed_password=bcrypt_context.hash(user_request.password),
        is_active=True
    )

    db.add(create_user_model)
    db.commit()

@router.post("/auth_token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):

    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return 'Failed authentication'
    return 'Successful authentication'