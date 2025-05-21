from fastapi import APIRouter
from .endpoints import auth, reader

router = APIRouter(prefix='/v1')

router.include_router(auth.router, tags=['Auth'])
router.include_router(reader.router, tags=['Readers'])