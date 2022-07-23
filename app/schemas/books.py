from pydantic import BaseModel


class Book(BaseModel):
    title: str
    pages: int
    author_id: int
    genre: str
    copies: int


class InsertBook(Book):
    pass


class UpdateBook(Book):
    pass


class ReturnBook(Book):
    id: int
