from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker
from ToDo_App.database.database import Base, get_db
from ..main import app
from ToDo_App.routers.auth import get_current_user

SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass= StaticPool
)

TestingSessionLocal = sessionmaker(autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

print(id(get_db))

def override_get_db():
    db = TestingSessionLocal()
    try: 
        yield db
    finally:
        db.close()


def override_get_current_user():
    return {
        "username": "test_user",
        "user_id": 1        
    }


app.dependency_overrides[get_current_user] = override_get_current_user
app.dependency_overrides[get_db] = override_get_db
