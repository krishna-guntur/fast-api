from fastapi import FastAPI
from database.database import engine
import database.database_models as database_models
from routers import auth, todos, users

app = FastAPI()
database_models.Base.metadata.create_all(engine)
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(users.router)

