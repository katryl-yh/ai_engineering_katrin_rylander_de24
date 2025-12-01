from fastapi import FastAPI, Query
from data_processing import library_data, Book
from pprint import pprint
from constants import CURRENT_YEAR

#Create the FastAPI application
app = FastAPI()

# Load book data from a file
library = library_data("library.json")
books = library.books
# Print the book list to the terminal so one can see what's loaded
pprint(books)

# Return all books
@app.get("/books")
async def read_books():
    return books

# Search books by exact title (case-insensitive)
# path parameter - before query params
@app.get("/books/title/{title}")
async def read_book_by_title(title: str):
    return [book for book in books if book.title.casefold() == title.casefold()]

# Return the book with a specific id
@app.get("/book/{id}")
async def read_book_by_id(id: int):
    return [book for book in books if book.id == id]

# Filter books using query parameters
# query parameter - ?start_year=1950
@app.get("/books/")
async def filter_books(
    start_year: int = Query(
        1950,
        gt=1500,
        lt=CURRENT_YEAR + 1,
        description="Filters books that are newer than this year",
    ),
    author: str = Query(None, description="Authors firstname and lastname "),
):
    filtered_books = [book for book in books if start_year < book.year]

    if author:
        filtered_books = [
            book
            for book in filtered_books
            if author.casefold() == book.author.casefold()
        ]

    return filtered_books

# Add a new book to the list
@app.post("/books/create_book")
async def create_book(book_request: Book):
    new_book = Book.model_validate(book_request)
    books.append(new_book)

    return new_book
# Update an existing book (matched by id)
@app.put("/books/update_book")
async def update_book(updated_book: Book):
    for i, book in enumerate(books):
        if book.id == updated_book.id:
            books[i] = updated_book
    return updated_book
# Deletes a book based on its ID
@app.delete("/books/delete_book/{id}")
async def delete_book(id: int):
    for i, book in enumerate(books):
        if book.id == id:
            del books[i]
            break