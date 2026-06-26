from fastapi import status
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import text

from .utils import *
from ToDo_App.database.database import get_db
from ..main import app
from ToDo_App.routers.auth import get_current_user
from ToDo_App.database.database_models import USERS

client = TestClient(app)

app.dependency_overrides[get_current_user] = override_get_current_user
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def testuser():
    
    user = USERS(
        email = 'email',
        username = 'username',
        first_name = 'first_name',
        last_name = 'last_name',
        role = 'role',
        hashed_password='password',
        is_active=True
    )

    db = TestingSessionLocal()
    db.add(user)
    db.commit()

    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM USERS;"))
        connection.commit()

def test_create_user(testuser):

    user_request = {
                        "email": "email",
                        "username": "username",
                        "first_name": "first_name",
                        "last_name": "last_name",
                        "role": "role",
                        "password": "password"
}

    response = client.post('/auth/create-user', json=user_request)
    assert response.status_code == 201