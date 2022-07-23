from fastapi import FastAPI

from app import books, users

app = FastAPI(title="Library Management")


app.include_router(users.router, prefix="/user", tags=["User"])
app.include_router(books.router, prefix="/book", tags=["Book"])


@app.get("/")
def greet(name: str = "User"):
    return {"message": f"Welcome {name}"}
