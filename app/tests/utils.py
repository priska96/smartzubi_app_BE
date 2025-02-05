import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from ..main import app
from ..database import get_db, Base
from ..feature.auth.auth_bearer import jwt_bearer

# In your test configuration, e.g., test_settings.py or directly in the test
SQLALCHEMY_DATABASE_URL = "postgresql://testuser:testpassword@localhost:5431/testdb"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


def override_jwt_bearer():
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzA5MjgzOTUsInN1YiI6IjE5In0.IRCCcAr5yw7Ogkpi-fBzDhPPweaW44lrmO4c6-ANLvM"


def token_required_no_op(func):
    return func


app.dependency_overrides[jwt_bearer] = override_jwt_bearer

client = TestClient(app)

