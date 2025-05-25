import read_book
from fastapi import FastAPI, HTTPException
from starlette.responses import JSONResponse
from models import Book
from pydantic import BaseModel

import json
from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse

app = FastAPI()

class BookResponse(BaseModel):
    title: str
    author: str

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return PlainTextResponse(
        "This is a plain text response:" f" \n{json.dumps(exc.errors(), indent=2)} ", status_code=status.HTTP_400_BAD_REQUEST
    )



@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": "Oops! Something went wrong."}
    )


@app.get("/error_endpoint")
async def raise_exception():
    raise HTTPException(status_code=400)


@app.get("/allbooks")
async def read_all_books() -> list[BookResponse]:
    return [
      {"id": 1, "title": "1984", "author": "George Orwell"},
      {"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald"}
    ]  

app.include_router(read_book.router)

@app.get("/authors/{author_id}")
async def read_author(author_id: int):
    return{
        "author_id": author_id,
        "name": "Ernest Hemingway"
    }

@app.get("/books")
async def read_books(year: int = None):
    if year:
        return [
            {"year": year, "books": ["Book 1", "Book 2"]}
        ]
    return {"books": ["All Books"] } 

@app.post("/book")
async def create_book(book: Book):
    return book


