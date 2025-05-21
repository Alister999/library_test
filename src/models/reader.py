from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column
from src.models.general import Base


class Reader(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True, index=True)
    name: Mapped[str] = mapped_column(index=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
