from fastapi import APIRouter


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