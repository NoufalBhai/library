from pydantic import BaseModel

class InsertBook(BaseModel):
    title: str
    pages: int
    author_id: int
    genre: str
    copies: int 