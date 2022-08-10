from fastapi import APIRouter, Depends, Response, status
from fastapi.responses import JSONResponse

from app.crud import users
from app.schemas import users as scuser
from app.utils.dep import get_user

router = APIRouter()


@router.post("/", response_model=scuser.ReturnUser)
def add_user(user: scuser.RegisterUser):
    """
    This Function Will Create a new user
    """
    return users.create(user)


@router.get("/", response_model=list[scuser.ReturnUser])
def get_all_users(limit: int = 3, offset: int = 0):
    all_users = users.get_all(offset, limit)
    print(all_users)
    return all_users


@router.get(
    "/{id}",
    response_model=scuser.ReturnUser,
    responses={
        200: {"model": scuser.RegisterUser},
        404: {"model": dict[str, str]},
    },
)
def get_user_by_id(id: int):
    user = users.get_one(id)
    if not user:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"message": "No User Found"}
        )
    return dict(user)


@router.delete("/{id}", status_code=204, response_class=Response)
def delete_user(id: int, _=Depends(get_user)):
    user = users.get_one(id)
    if not user:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"message": "No User Found"}
        )
    users.delete(id)
    return None


@router.put("/{id}", response_model=scuser.ReturnUser)
def update_user(id: int, user: scuser.BaseUser, _=Depends(get_user)):
    user_in_db = users.get_one(id)
    if not user_in_db:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"message": "No User Found"}
        )
    changed_user_in_db = users.update(user)
    return dict(changed_user_in_db)
