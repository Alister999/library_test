import logging
from typing import List
from fastapi import APIRouter
from src.core.dependencies import SessionDep, AuthDep
from src.schemas.readers import ReaderCreate, ReaderResponse
from src.services.reader_service import create_reader, delete_this_reader, get_readers_all, get_this_reader, \
    change_this_reader

router = APIRouter()
logger = logging.getLogger('ReaderEndpoint')

@router.post('/reader', response_model=ReaderResponse)
async def add_reader(data: ReaderCreate, db: SessionDep, current_user: AuthDep) -> ReaderResponse:
    logger.info('Calling post reader endpoint')
    result = await create_reader(data, db)
    return result


@router.delete('/reader/{reader_id}')
async def delete_reader(reader_id: int, db: SessionDep, current_user: AuthDep) -> dict[str, str] | None:
    logger.info('Calling delete reader endpoint')
    result = await delete_this_reader(reader_id, db)
    if result:
        return {'message': f'Reader with id {reader_id} was deleted successful'}


@router.get('/reader', response_model=List[ReaderResponse])
async def get_readers(db: SessionDep, current_user: AuthDep) -> List[ReaderResponse]:
    logger.info('Calling get readers endpoint')
    result = await get_readers_all(db)
    return result


@router.get('/reader/{reader_id}', response_model=ReaderResponse)
async def get_reader(reader_id: int, db: SessionDep, current_user: AuthDep) -> ReaderResponse:
    logger.info('Calling get reader endpoint')
    result = await get_this_reader(reader_id, db)
    return result


@router.put('/reader/{reader_id}', response_model=ReaderResponse)
async def change_reader(data: ReaderCreate, reader_id: int, db: SessionDep, current_user: AuthDep) -> ReaderResponse:
    logger.info('Calling change reader endpoint')
    result = await change_this_reader(data, reader_id, db)
    return result