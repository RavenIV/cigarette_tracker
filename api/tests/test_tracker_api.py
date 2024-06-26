from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from tracker_api.database import Base
from tracker_api.main import app, get_db


SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

FORM_DATA = {'telegram_id': 12345}


def test_create_user():
    response = client.post("users/", json=FORM_DATA)
    assert response.status_code == 200, response.text
    data = response.json()
    assert 'id' in data
    user_id = data['id']

    response = client.get(f"users/{user_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['id'] == user_id
    assert data['telegram_id'] == FORM_DATA['telegram_id']
