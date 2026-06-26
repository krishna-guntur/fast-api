from fastapi import FastAPI
from ToDo_App.database.database import engine
import ToDo_App.database.database_models as database_models
from ToDo_App.routers import auth, todos, users

app = FastAPI()

database_models.Base.metadata.create_all(engine)

@app.get("/health-check")
def health_check():
    return {"status": "healthy"}


app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(users.router)

