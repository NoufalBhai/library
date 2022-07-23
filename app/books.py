from fastapi import APIRouter, HTTPException, Response, status
from psycopg2.extras import DictCursor

from app.db import conn
from app.schemas import books

router = APIRouter()


@router.get("/", response_model=list[books.ReturnBook])
def get_all_books():
    query = """
    SELECT * FROM library.books"""

    cursor = conn.cursor(cursor_factory=DictCursor)
    cursor.execute(query)
    all_books = cursor.fetchall()
    cursor.close()
    return [dict(book) for book in all_books]


@router.post("/")
def add_book(book: books.InsertBook):
    query = """
    Insert into library.books(title, pages, author_id, genre, copies)
    values(%s, %s, %s, %s, %s) returning * """
    params = (book.title, book.pages, book.author_id, book.genre, book.copies)
    try:
        cursor = conn.cursor(cursor_factory=DictCursor)

        cursor.execute(query, params)
        conn.commit()
        new_book = cursor.fetchone()
        cursor.close()
    except Exception:
        conn.rollback()
        raise HTTPException(status_code=500, detail="internal server error")
    finally:
        cursor.close()

    return dict(new_book)


@router.put("/{id}")
def update_books(id: int, updatebook: books.UpdateBook):
    query = """ SELECT * FROM LIBRARY.books WHERE id=%s;"""
    params = (id,)

    cursor = conn.cursor(cursor_factory=DictCursor)

    cursor.execute(query, params)
    old_book = cursor.fetchone()
    if not old_book:

        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Book not Found")

    query = """ SELECT * FROM LIBRARY.author WHERE id=%s;"""
    params = (updatebook.author_id,)

    cursor = conn.cursor(cursor_factory=DictCursor)

    cursor.execute(query, params)
    author_exist = cursor.fetchone()
    if not author_exist:

        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Author not Found")

    query = """UPDATE library.books SET title=%s, pages=%s, author_id= %s, copies= %s WHERE id=%s RETURINING * ;"""
    params = (
        updatebook.title,
        updatebook.pages,
        updatebook.author_id,
        updatebook.copies,
        id,
    )

    cursor = conn.cursor(cursor_factory=DictCursor)

    cursor.execute(query, params)
    conn.commit()
    new_book = cursor.fetchone()
    return dict(new_book)


@router.get("/{id}", response_model=books.ReturnBook)
def get_one(id: int):
    query = "SELECT * FROM library.books WHERE id = %s"
    params = (id,)
    cursor = conn.cursor(cursor_factory=DictCursor)
    cursor.execute(query, params)
    books = cursor.fetchone()
    cursor.close()
    return dict(books)


@router.delete("/{id}", response_class=Response, status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int):
    query = "DELETE FROM library.books WHERE id = %s"
    params = (id,)
    cursor = conn.cursor(cursor_factory=DictCursor)
    cursor.execute(query, params)
    conn.commit()
    cursor.close()
    return None
