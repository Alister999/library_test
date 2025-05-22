import logging
from typing import List
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import ReaderRepository
from src.models.reader import Reader
from src.schemas.readers import ReaderCreate, ReaderResponse

logger = logging.getLogger("ReaderService")


async def create_reader(data: ReaderCreate, db: AsyncSession) -> ReaderResponse:
    repo = ReaderRepository(session=db)
    logger.info("Incoming to create reader func")
    if await repo.get_one_or_none(Reader.email == data.email):
        logger.warning(f"Reader with email {data.email} already exist")
        raise HTTPException(
            status_code=403,
            detail=f"Reader with email {data.email} already exist"
        )
    new_reader = Reader(
        name=data.name,
        email=data.email
    )

    logger.info("Add reader to repo")
    await repo.add(new_reader)
    await db.commit()
    await db.refresh(new_reader)

    return ReaderResponse.model_validate(new_reader)


async def delete_this_reader(reader_id: int, db: AsyncSession) -> bool:
    logger.info("Incoming to delete reader func")
    repo = ReaderRepository(session=db)
    getting_reader = await repo.get_one_or_none(Reader.id == reader_id)
    if not getting_reader:
        logger.warning(f"Reader with id '{reader_id}' is absent")
        raise HTTPException(
            status_code=404,
            detail=f"Reader with id '{reader_id}' is absent"
        )
    logger.info("Delete reader from repo")
    await repo.delete(reader_id)
    await db.commit()
    return True


async def get_readers_all(db: AsyncSession) -> List[ReaderResponse]:
    logger.info("Incoming to get readers func")
    repo = ReaderRepository(session=db)
    db_readers = await repo.list()
    re_formatted_readers = (ReaderResponse.model_validate(db_reader) for db_reader in db_readers)
    return list(re_formatted_readers)


async def get_this_reader(reader_id: int, db: AsyncSession) -> ReaderResponse:
    logger.info("Incoming to get reader func")
    repo = ReaderRepository(session=db)
    getting_reader = await repo.get_one_or_none(Reader.id == reader_id)
    if not getting_reader:
        logger.warning(f"Reader with id '{reader_id}' is absent")
        raise HTTPException(
            status_code=404,
            detail=f"Reader with id '{reader_id}' is absent"
        )
    re_formatted_reader = ReaderResponse.model_validate(getting_reader)
    return re_formatted_reader


async def change_this_reader(data: ReaderCreate, reader_id: int, db: AsyncSession) -> ReaderResponse:
    logger.info("Incoming to change reader func")
    repo = ReaderRepository(session=db)
    changeable_reader = await repo.get_one_or_none(Reader.id == reader_id)
    if not changeable_reader:
        logger.warning(f"Reader with id '{reader_id}' is absent")
        raise HTTPException(
            status_code=404,
            detail=f"Reader with id '{reader_id}' is absent"
        )
    if await repo.get_one_or_none(Reader.email == data.email):
        logger.warning(f"Reader with email '{data.email}' already exist")
        raise HTTPException(
            status_code=404,
            detail=f"Reader with name '{data.email}' already exist"
        )
    for key, value in data.model_dump().items():
        if key != "id":
            setattr(changeable_reader, key, value)

    logger.info("Update reader to repo")
    await repo.update(changeable_reader)
    await db.commit()
    await db.refresh(changeable_reader)

    re_formatted_reader = ReaderResponse.model_validate(changeable_reader)
    return re_formatted_reader