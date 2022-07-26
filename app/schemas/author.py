from pydantic import BaseModel


class AuthorID(BaseModel):
    id: int


class Author(BaseModel):
    name: str
    description: str


class ReturnAuthor(Author, AuthorID):
    pass
