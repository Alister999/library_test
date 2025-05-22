import logging
from typing import List
from fastapi import APIRouter
from src.core.dependencies import SessionDep, AuthDep
from src.schemas.books import BookResponse, BookCreate
from src.services.book_service import create_book, delete_this_book, get_books_all, get_this_book, change_this_book

router = APIRouter()
logger = logging.getLogger('BookEndpoint')


@router.post('/book', response_model=BookResponse)
async def add_reader(data: BookCreate, db: SessionDep, current_user: AuthDep) -> BookResponse:
    logger.info('Calling post book endpoint')
    result = await create_book(data, db)
    return result


@router.delete('/book/{book_id}')
async def delete_book(book_id: int, db: SessionDep, current_user: AuthDep) -> dict[str, str] | None:
    logger.info('Calling delete book endpoint')
    result = await delete_this_book(book_id, db)
    if result:
        return {'message': f'Book with id {book_id} was deleted successful'}


@router.get('/book', response_model=List[BookResponse])
async def get_books(db: SessionDep, current_user: AuthDep) -> List[BookResponse]:
    logger.info('Calling get books endpoint')
    result = await get_books_all(db)
    return result


@router.get('/book/{book_id}', response_model=BookResponse)
async def get_book(book_id: int, db: SessionDep, current_user: AuthDep) -> BookResponse:
    logger.info('Calling get book endpoint')
    result = await get_this_book(book_id, db)
    return result


@router.put('/book/{book_id}', response_model=BookResponse)
async def change_book(data: BookCreate, book_id: int, db: SessionDep, current_user: AuthDep) -> BookResponse:
    logger.info('Calling change book endpoint')
    result = await change_this_book(data, book_id, db)
    return result