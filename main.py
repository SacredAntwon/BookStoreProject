# Authors: Anthony Maida and Steven Burroughs
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from bson.objectid import ObjectId
from typing import List, Optional

# Declarations for the app, database, and collection
app = FastAPI()
mongo_client = AsyncIOMotorClient("mongodb://localhost:27017")
db = mongo_client["bookstore"]
books_collection = db["books"]

# Create a model for the book using pydantic
class Book(BaseModel):
    title: str
    author: str
    description: str
    price: float
    stock: int

class BookInDB(Book):
    id: str

def book_helper(book) -> BookInDB:
    return BookInDB(**book, id=str(book["_id"]))

# Indexes to improve performance
@app.on_event("startup")
async def startup_event():
    await books_collection.create_index("title")
    await books_collection.create_index("author")
    await books_collection.create_index("price")

# Aggregate to get the total stock
@app.get("/stock")
async def get_total_stock():
    cursor = books_collection.aggregate([{"$group": {"_id": None, "total_books": {"$sum": "$stock"}}}])
    result = await cursor.to_list(length=1)
    return result[0] if result else {"total_books": 0}

##### TO DO #####
##### FIGURE WHICH VERSION TO USE FOR AUTHORS WITH MOST BOOKS #####
# Aggregate to find authors total books
# Get number of books by the same author
# @app.get("/authorswithmostbooks")
# async def get_authors_most_books():
#     cursor = books_collection.aggregate([{"$group": {"_id": "$author", "count": { "$sum": 1 }}},{"$sort": { "count": -1 }},{"$limit": 5}])
#     result = await cursor.to_list(length=None)
#     return result if result else {"count": 0}   

# This version gets the stock of the author
@app.get("/authorswithmostbooks")
async def get_authors_most_books():
    cursor = books_collection.aggregate([{"$group": {"_id": "$author", "count": { "$sum": "$stock" }}},{"$sort": { "count": -1 }},{"$limit": 5}])
    result = await cursor.to_list(length=None)
    return result if result else {"count": 0}

##### TO DO #####
##### FIGURE WHICH VERSION TO USE FOR BEST SELLING BOOK #####
# This version finds books with the least stock to show it is the best selling book
@app.get("/bestsellingbooks")
async def get_best_selling_book():
    cursor = books_collection.aggregate([{"$group": {"_id": "$title", "count": { "$sum": "$stock" }}},{"$sort": { "count": 1 }},{"$limit": 5}])
    result = await cursor.to_list(length=None)
    return result if result else {"count": 0}

# Get all books
@app.get("/books", response_model=List[BookInDB])
async def get_books():
    books = []
    async for book in books_collection.find():
        books.append(book_helper(book))
    return books

# Get book by id
@app.get("/books/{book_id}", response_model=BookInDB)
async def get_book(book_id: str):
    book = await books_collection.find_one({"_id": ObjectId(book_id)})
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book_helper(book)

# Create a new book
@app.post("/books", response_model=BookInDB)
async def create_book(book: Book):
    new_book = await books_collection.insert_one(book.dict())
    created_book = await books_collection.find_one({"_id": new_book.inserted_id})
    return book_helper(created_book)

# Update a book
@app.put("/books/{book_id}", response_model=BookInDB)
async def update_book(book_id: str, book: Book):
    updated_book = await books_collection.find_one_and_replace({"_id": ObjectId(book_id)}, book.dict())
    if not updated_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book_helper(updated_book)

# Delete a book
@app.delete("/books/{book_id}")
async def delete_book(book_id: str):
    result = await books_collection.delete_one({"_id": ObjectId(book_id)})
    if not result.deleted_count:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book successfully deleted"}

# Search books by title, author, price
@app.get("/search", response_model=List[BookInDB])
async def search_books(title: Optional[str] = None, author: Optional[str] = None, min_price: Optional[float] = None, max_price: Optional[float] = None):
    query = {}
    if title:
        query["title"] = {"$regex": title, "$options": "i"}
    if author:
        query["author"] = {"$regex": author, "$options": "i"}
    if min_price is not None and max_price is not None:
        query["price"] = {"$gte": min_price, "$lte": max_price}
    elif min_price:
        query["price"] = {"$gte": min_price}
    elif max_price:
        query["price"] = {"$lte": max_price}

    books = []
    async for book in books_collection.find(query):
        books.append(book_helper(book))
    return books

# Main to run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info")
