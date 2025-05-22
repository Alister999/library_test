from fastapi import APIRouter
from .endpoints import auth, reader, book

router = APIRouter(prefix='/v1')

router.include_router(auth.router, tags=['Auth'])
router.include_router(reader.router, tags=['Readers'])
router.include_router(book.router, tags=['Books'])