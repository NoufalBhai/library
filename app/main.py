from fastapi import FastAPI

from app.api import auth, author, books, users

app = FastAPI(title="Library Management")


app.include_router(users.router, prefix="/user", tags=["User"])
app.include_router(books.router, prefix="/book", tags=["Book"])
app.include_router(author.router, prefix="/author", tags=["Author"])
app.include_router(auth.router, prefix="/auth", tags=["Authenticaton"])


@app.get("/")
def greet(name: str = "User"):
    return {"message": f"Welcome {name}"}
