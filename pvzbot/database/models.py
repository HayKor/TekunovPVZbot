from sqlalchemy import Boolean, Integer, String
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(
        "id", Integer(), primary_key=True, autoincrement=True
    )
    nickname: Mapped[str] = mapped_column("nickname", String(), nullable=False)
    is_admin: Mapped[bool] = mapped_column("is_admin", Boolean(), default=False)
    is_father: Mapped[bool] = mapped_column("is_father", Boolean(), default=False)


class Points(Base):
    __tablename__ = "points"
    id: Mapped[int] = mapped_column(
        "id", Integer(), primary_key=True, autoincrement=True
    )
    address: Mapped[str] = mapped_column("address", String(), nullable=False)
    type: Mapped[str] = mapped_column("type", String(), nullable=False)
