import logging
from typing import List
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import ReaderRepository, BookRepository
from src.models.book import Book
from src.schemas.books import BookCreate, BookResponse

logger = logging.getLogger("BookService")


async def create_book(data: BookCreate, db: AsyncSession) -> BookResponse:
    repo = BookRepository(session=db)
    logger.info("Incoming to create book func")
    find_book = await repo.get_one_or_none(
        Book.name == data.name,
        Book.author == data.author,
        Book.year == data.year,
        Book.ISBN == data.ISBN
    )

    if find_book:
        logger.info(f"Find the book by same name, author, year and ISBN with ID {find_book.id}")
        find_book.count += 1
        logger.info(f"Increment count of finding book to repo with ID {find_book.id}")
        await repo.update(find_book)
        await db.commit()
        await db.refresh(find_book)
        re_formatted_book = BookResponse.model_validate(find_book)
        return re_formatted_book

    new_book = Book()
    for key, value in data.model_dump().items():
        if key != "id":
            setattr(new_book, key, value)
    logger.info("Add reader to repo")
    await repo.add(new_book)
    await db.commit()
    await db.refresh(new_book)
    re_formatted_book = BookResponse.model_validate(new_book)
    return re_formatted_book


async def delete_this_book(book_id: int, db: AsyncSession) -> bool:
    logger.info("Incoming to delete book func")
    repo = BookRepository(session=db)
    getting_book = await repo.get_one_or_none(Book.id == book_id)
    if not getting_book:
        logger.warning(f"Book with id '{book_id}' is absent")
        raise HTTPException(
            status_code=404,
            detail=f"Book with id '{book_id}' is absent"
        )
    logger.info("Delete Book from repo")
    await repo.delete(book_id)
    await db.commit()
    return True


async def get_books_all(db: AsyncSession) -> List[BookResponse]:
    logger.info("Incoming to get books func")
    repo = BookRepository(session=db)
    db_books = await repo.list()
    re_formatted_books = (BookResponse.model_validate(db_book) for db_book in db_books)
    return list(re_formatted_books)


async def get_this_book(book_id: int, db: AsyncSession) -> BookResponse:
    logger.info("Incoming to get book func")
    repo = BookRepository(session=db)
    getting_book = await repo.get_one_or_none(Book.id == book_id)
    if not getting_book:
        logger.warning(f"Book with id '{book_id}' is absent")
        raise HTTPException(
            status_code=404,
            detail=f"Book with id '{book_id}' is absent"
        )
    re_formatted_book = BookResponse.model_validate(getting_book)
    return re_formatted_book


async def change_this_book(data: BookCreate, book_id: int, db: AsyncSession) -> BookResponse:
    logger.info("Incoming to change book func")
    repo = BookRepository(session=db)
    changeable_book = await repo.get_one_or_none(Book.id == book_id)
    if not changeable_book:
        logger.warning(f"Book with id '{book_id}' is absent")
        raise HTTPException(
            status_code=404,
            detail=f"Book with id '{book_id}' is absent"
        )
    if await repo.get_one_or_none(Book.name == data.name):
        logger.warning(f"Book with name '{data.name}' already exist")
        raise HTTPException(
            status_code=404,
            detail=f"Book with name '{data.name}' already exist"
        )
    if await repo.get_one_or_none(Book.year == data.year):
        logger.warning(f"Book with year '{data.year}' already exist")
        raise HTTPException(
            status_code=404,
            detail=f"Book with year '{data.year}' already exist"
        )
    if await repo.get_one_or_none(Book.author == data.author):
        logger.warning(f"Book with author '{data.author}' already exist")
        raise HTTPException(
            status_code=404,
            detail=f"Book with author '{data.author}' already exist"
        )
    if await repo.get_one_or_none(Book.ISBN == data.ISBN):
        logger.warning(f"Book with ISBN '{data.ISBN}' already exist")
        raise HTTPException(
            status_code=404,
            detail=f"Book with ISBN '{data.ISBN}' already exist"
        )
    for key, value in data.model_dump().items():
        if key != "id":
            setattr(changeable_book, key, value)
    logger.info("Update book to repo")
    await repo.update(changeable_book)
    await db.commit()
    await db.refresh(changeable_book)

    re_formatted_book = BookResponse.model_validate(changeable_book)
    return re_formatted_book