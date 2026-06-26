from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:090909@localhost/postgres'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
local_session = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()

def get_db():
    db = local_session()
    try:
        yield db
    finally:
        db.close()

