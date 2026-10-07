from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Library API")

# База данных в памяти (In-Memory)
books_db = [
    {"id": 1, "title": "1984", "author": "Джордж Оруэлл", "year": 1949},
    {"id": 2, "title": "Мастер и Маргарита", "author": "Михаил Булгаков", "year": 1967}
]

current_id = 2

class BookCreate(BaseModel):
    title: str
    author: str
    year: int

class Book(BaseModel):
    id: int
    title: str
    author: str
    year: int

@app.get("/books", response_model=List[Book])
def get_books():
    return books_db

@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    for book in books_db:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Книга не найдена")

@app.post("/books", response_model=Book, status_code=status.HTTP_201_CREATED)
def create_book(book_data: BookCreate):
    global current_id
    current_id += 1
    new_book = {
        "id": current_id,
        "title": book_data.title,
        "author": book_data.author,
        "year": book_data.year
    }
    books_db.append(new_book)
    return new_book

@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, book_data: BookCreate):
    for book in books_db:
        if book["id"] == book_id:
            book["title"] = book_data.title
            book["author"] = book_data.author
            book["year"] = book_data.year
            return book
    raise HTTPException(status_code=404, detail="Книга не найдена")

@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int):
    for index, book in enumerate(books_db):
        if book["id"] == book_id:
            books_db.pop(index)
            return
    raise HTTPException(status_code=404, detail="Книга не найдена")
