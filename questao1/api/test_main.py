import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_biblioteca.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_register_book():
    payload = {
        "title": "A Court of Thorns and Roses",
        "author": "Sarah J. Maas",
        "public_date": "2015-05-05",
        "summary": "A Court of Thorns and Roses is a fantasy romance series by American author Sarah J. Maas, which follows the journey of 19-year-old Feyre Archeron after she is brought into the faerie lands of Prythian. The first book of the series, A Court of Thorns and Roses, was released in May 2015"
    }
    response = client.post("/books/", json=payload)
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "A Court of Thorns and Roses"
    assert "id" in data

def test_search_books_no_filter():
    response = client.get("/books/")
    assert response.status_code == 200
    # precisa ter 1 livro por conta do test_register_book
    assert len(response.json()) >= 1

def test_search_books_filter_author():
    response = client.get("/books/?author=Sarah")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["author"] == "Sarah J. Maas"

def test_search_books_filter_title_inexistent():
    response = client.get("/books/?title=BookQueNaoExiste")
    assert response.status_code == 200
    assert response.json() == []