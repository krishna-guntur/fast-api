from fastapi import FastAPI, APIRouter

Users = APIRouter()

@Users.get("/get-user")
async def get_user():
    pass