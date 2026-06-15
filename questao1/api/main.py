from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

import models
import schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/books/", response_model=schemas.BookResponse, status_code=201)
def register_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_book = models.Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    
    return db_book

@app.get("/books/", response_model=List[schemas.BookResponse])
def search_books(
    title: Optional[str] = Query(None, description="Filtrar por parte do título"),
    author: Optional[str] = Query(None, description="Filtrar por parte do nome do author"),
    db: Session = Depends(get_db)
):
    query = db.query(models.Book)
    
    if title:
        query = query.filter(models.Book.title.ilike(f"%{title}%"))
    if author:
        query = query.filter(models.Book.author.ilike(f"%{author}%"))
        
    return query.all()