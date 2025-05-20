from fastapi import APIRouter
from .endpoints import auth, entity

router = APIRouter(prefix='/v1')

router.include_router(auth.router, tags=['Auth'])
# router.include_router(entity.router, tags=['Entity'])