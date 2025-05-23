import logging
import os
from typing import Any, AsyncGenerator

from src.models.book import Book
from src.models.reader import Reader

IS_TEST = os.getenv("IS_TEST") == "1"

from advanced_alchemy.config import SQLAlchemyAsyncConfig
from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from dotenv import load_dotenv

from src.models.general import Base
from src.models.user import User
from src.core.config import settings

load_dotenv()
logger = logging.getLogger("DB")

db_config: SQLAlchemyAsyncConfig | None = None

def get_config() -> SQLAlchemyAsyncConfig:
    is_test = os.getenv("IS_TEST") == "1"
    logger.info(f"IS_TEST = {is_test}")
    url = (
        f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.TEST_DB_HOST}:5432/{settings.TEST_DB_NAME}"
        if is_test
        else f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:5432/{settings.DB_NAME}"
    )
    return SQLAlchemyAsyncConfig(connection_string=url)

sync_database_url = f"postgresql+psycopg2://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:5432/{settings.DB_NAME}"


async def get_db() -> AsyncGenerator[Any, Any]:
    logger.info("Try to get DB")
    config = get_config()
    async with config.get_session() as session:
        yield session


async def init_db():
    logger.info("Try to init DB")
    config = get_config()
    async with config.get_engine().begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


class UserRepository(SQLAlchemyAsyncRepository[User]):
    model_type = User

class ReaderRepository(SQLAlchemyAsyncRepository[Reader]):
    model_type = Reader

class BookRepository(SQLAlchemyAsyncRepository[Book]):
    model_type = Book