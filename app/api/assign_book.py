from fastapi import APIRouter, HTTPException, status
from psycopg2.extras import DictCursor
from app.db import conn
from app.crud.users import get_one
from app.crud.books import get_by_id

router = APIRouter()


@router.post("/{user_id}/assign/{book_id}/")
def assign_book_to_user(user_id: int, book_id: int):
    user = get_one(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not Found"
        )
    book = get_by_id(book_id)
    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book Not Found"
        )
    query = "INSERT INTO library.books_taken(user_id, book_id) VALUES(%s, %s) RETURNING *;"
    values = (user_id, book_id)
    try:
        cursor = conn.cursor(cursor_factory=DictCursor)
        cursor.execute(query, values)
        conn.commit()
        assigned_book = cursor.fetchone()
    except Exception as ex:
        print(ex)
        conn.rollback()
        raise HTTPException(status_code=500, detail="Database Issue")
    else:
        return dict(assigned_book)
    finally:
        cursor.close()
    
    