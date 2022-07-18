
from fastapi import APIRouter,HTTPException

from app.schemas import books
from app.db import conn
from psycopg2.extras import DictCursor


all_books = [
    "Book1",
    "Book2",
    "Book3",
    "Book4",
]

router = APIRouter()



@router.get("/")
def get_all_books():
    return all_books

@router.post("/")
def add_book(book: books.InsertBook):
    query= """
    Insert into library.books(title, pages, author_id, genre, copies)
    values(%s, %s, %s, %s, %s) returning * """
    params=(book.title, book.pages, book.author_id, book.genre, book.copies)
    try:
        cursor=conn.cursor(cursor_factory=DictCursor)

        cursor.execute(query,params)
        conn.commit()
        new_book=cursor.fetchone()
        cursor.close()
    except Exception: 
        conn.rollback()
        raise HTTPException(status_code=500,detail="internal server error")
    finally: 
        cursor.close()

    return dict(new_book)