from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from fastapi.testclient import TestClient

client = TestClient(app)
SQLALCHEMY_DATABASE_URL = "sqlite:///test.sqlite"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL, echo=True, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

URL_BASE = "/api/v1"


def test_get_products_unauthorized():
    STATUS_RESPONSE = 401
    response = client.get(f"{URL_BASE}/products/get")

    assert response.status_code == STATUS_RESPONSE


def test_get_products_authorized():
    STATUS_RESPONSE = 200

    response_login = client.post(
        f"{URL_BASE}/auth/login",
        json={"email": "test@email.com", "password": "1234567S_*"},
    )

    token = dict(response_login.json()).get("access_token")

    headers = {"Authorization": f"Bearer {token}"}

    response = client.get(f"{URL_BASE}/products/get", headers=headers)

    assert response.status_code == STATUS_RESPONSE
