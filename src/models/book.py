from sqlalchemy.orm import Mapped, mapped_column

from src.models.general import Base


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True, index=True)
    name: Mapped[str] = mapped_column(index=True, nullable=False)
    author: Mapped[str] = mapped_column(index=True, nullable=False)
    year: Mapped[int] = mapped_column(nullable=True)
    ISBN: Mapped[str] = mapped_column(unique=True, nullable=True)
    count: Mapped[int] = mapped_column(default=1)