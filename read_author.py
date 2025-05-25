from fastapi import APIRouter
router = APIRouter()
@app.get("/authors/{author_id}")
async def read_author(author_id: int):
    return{
        "author_id": author_id,
        "name": "Ernest Hemingway"
    } 
