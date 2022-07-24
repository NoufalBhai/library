from fastapi import APIRouter, HTTPException, Response, status
from psycopg2.extras import DictCursor

from app.db import conn
from app.schemas import books
from app.crud import books as bks

router = APIRouter()


@router.get("/", response_model=list[books.ReturnBook])
def get_all_books():
    return bks.get_all_books()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=books.ReturnBook)
def add_book(book: books.InsertBook):
    new_book = bks.create(book)
    return dict(new_book)


@router.put("/{id}")
def update_books(id: int, updatebook: books.UpdateBook):
    old_book = bks.get_by_id(id)
    if not old_book:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Book not Found")

    query = """ SELECT * FROM LIBRARY.author WHERE id=%s;"""
    params = (updatebook.author_id,)

    cursor = conn.cursor(cursor_factory=DictCursor)

    cursor.execute(query, params)
    author_exist = cursor.fetchone()
    if not author_exist:

        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Author not Found")
    new_book = bks.update(id, updatebook)
    return dict(new_book)


@router.get("/{id}", response_model=books.ReturnBook)
def get_one(id: int):
    book = bks.get_by_id(id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No Book Found"
        )
    return dict(book)


@router.delete("/{id}", response_class=Response, status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int):
    old_book = bks.get_by_id(id)
    if not old_book:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Book not Found")
    
    return bks.delete()
