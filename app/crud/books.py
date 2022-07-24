from fastapi import HTTPException
from psycopg2.extras import DictCursor

from app.db import conn
from app.schemas import books

def create(book: books.InsertBook):
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
    return new_book

def get_by_id(id: int):
    query = "SELECT * FROM library.books WHERE id = %s"
    params = (id,)
    cursor = conn.cursor(cursor_factory=DictCursor)
    cursor.execute(query, params)
    book = cursor.fetchone()
    cursor.close()
    return book

def get_all_books():
    query = """SELECT * FROM library.books"""
    cursor = conn.cursor(cursor_factory=DictCursor)
    cursor.execute(query)
    all_books = cursor.fetchall()
    cursor.close()
    return [dict(book) for book in all_books]

def delete(id):
    query = "DELETE FROM library.books WHERE id = %s"
    params = (id,)
    cursor = conn.cursor(cursor_factory=DictCursor)
    cursor.execute(query, params)
    conn.commit()
    cursor.close()
    
def update(id: int, book: books.UpdateBook):
    query = """
    UPDATE library.books 
        SET title=%s,
        pages=%s,
        author_id= %s,
        copies= %s 
    WHERE id=%s 
    RETURINING * ;"""
    params = (
        book.title,
        book.pages,
        book.author_id,
        book.copies,
        id,
    )

    cursor = conn.cursor(cursor_factory=DictCursor)

    cursor.execute(query, params)
    conn.commit()
    new_book = cursor.fetchone()
    return new_book