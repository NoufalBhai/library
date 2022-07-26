from psycopg2.extras import DictCursor

from app.db import conn
from app.schemas import author


def create(author: author.Author):
    query = "INSERT INTO library.author(name, description) VALUES (%s, %s) RETURNING *;"
    params = (author.name, author.description)
    cursor = conn.cursor(cursor_factory=DictCursor)
    cursor.execute(query, params)
    new_author = cursor.fetchone()
    conn.commit()
    cursor.close()
    return new_author


def get(id: int):
    query = "SELECT * FROM library.author WHERE id=%s;"
    params = (id,)
    cursor = conn.cursor(cursor_factory=DictCursor)
    cursor.execute(query, params)
    author = cursor.fetchone()
    cursor.close()
    return author


def get_all():
    query = "SELECT * FROM library.author;"
    cursor = conn.cursor(cursor_factory=DictCursor)
    cursor.execute(query)
    authors = cursor.fetchall()
    cursor.close()
    return [dict(author) for author in authors]


def update(id: int, author: author.Author):
    query = "UPDATE library.author SET name=%s, description=%s WHERE id=%s RETURNING *;"
    params = (author.name, author.description, id)
    cursor = conn.cursor(cursor_factory=DictCursor)
    cursor.execute(query, params)
    conn.commit()
    updated_author = cursor.fetchone()
    cursor.close()
    return updated_author


def delete(id: int):
    query = "DELETE FROM library.author WHERE id=%s;"
    params = (id,)
    cursor = conn.cursor(cursor_factory=DictCursor)
    cursor.execute(query, params)
    conn.commit()
    cursor.close()
