from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.crud import author as athr
from app.schemas import author
from app.utils.dep import get_librarian

router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=author.ReturnAuthor,
)
def create_author(author: author.Author, librarian=Depends(get_librarian)):
    new_author = athr.create(author)
    return dict(new_author)


@router.get("/", response_model=list[author.ReturnAuthor])
def get_all_author():
    authors = athr.get_all()
    return authors


@router.get("/{id}", response_model=author.ReturnAuthor)
def get_author(id: int):
    author_in_db = athr.get(id)
    if not author_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Author Not Found"
        )
    return dict(author_in_db)


@router.put("/{id}", response_model=author.ReturnAuthor)
def update_author(id: int, author_in: author.Author, librarian=Depends(get_librarian)):
    author_in_db = athr.get(id)
    if not author_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Author Not Found"
        )
    updated_author = athr.update(id, author_in)
    return dict(updated_author)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def delete_author(id: int, librarian=Depends(get_librarian)):
    author_in_db = athr.get(id)
    if not author_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Author Not Found"
        )
    return athr.delete(id)
