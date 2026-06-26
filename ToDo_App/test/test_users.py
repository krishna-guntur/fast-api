from fastapi import status
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import text
from pprint import pprint

from .utils import *
from ToDo_App.database.database import get_db
from ..main import app
from ToDo_App.routers.auth import get_current_user
from ToDo_App.database.database_models import USERS

client = TestClient(app)

app.dependency_overrides[get_current_user] = override_get_current_user
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def test_user():

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


def test_get_user(test_user):

    response = client.get("/users/get-user")
    assert response.status_code == 200

def test_change_password(test_user):

    response = client.put("/users/change-password?new_password=abcd1234")
    assert response.status_code == 200