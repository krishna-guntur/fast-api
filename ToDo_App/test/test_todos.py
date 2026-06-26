from fastapi import status
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import text
from pprint import pprint

from .utils import *
from ToDo_App.database.database import get_db
from ..main import app
from ToDo_App.routers.auth import get_current_user
from ToDo_App.database.database_models import TODOS

client = TestClient(app)

app.dependency_overrides[get_current_user] = override_get_current_user
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def test_todo():
    todo = TODOS(
        title='Test Title',
        description = "Test desc",
        priority = 1,
        complete = False,
        owner_id = 1
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()

    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM TODOS;"))
        connection.commit()

def test_get_all_todos(test_todo):

    response = client.get("/todos/get_todos")
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
        "id": 1,
        "title": "Test Title",
        "description": "Test desc",
        "priority": 1,
        "complete": False,
        "owner_id": 1
        }]
    
def test_get_todo(test_todo):

    response = client.get("/todos/get_todos/1")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": 1,
        "title": "Test Title",
        "description": "Test desc",
        "priority": 1,
        "complete": False,
        "owner_id": 1
        }
    
def test_create_to(test_todo):

    request = {        
        "title": "Test Title",
        "description": "Test desc",
        "priority": 1,
        "complete": False,        
        }

    response = client.post("/todos/create_todo", json=request)
    assert response.status_code == 201

def test_update_todo(test_todo):

    request = {        
        "title": "Test Title PUT",
        "description": "Test desc",
        "priority": 3,
        "complete": False,        
        }

    response = client.put("/todos/update_todo/1", json=request)
    assert response.status_code == 202

def test_delete_todo(test_todo):

    response = client.delete("/todos/delete_todo/1")
    assert response.status_code == 204