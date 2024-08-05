from sqlalchemy import Boolean, Integer, String
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column("id", Integer(), primary_key=True)
    nickname: Mapped[str] = mapped_column("nickname", String(), nullable=False)
    is_admin: Mapped[bool] = mapped_column("is_admin", Boolean(), default=False)
    is_father: Mapped[bool] = mapped_column(
        "is_father", Boolean(), default=False
    )


class Points(Base):
    __tablename__ = "points"
    id: Mapped[int] = mapped_column(
        "id", Integer(), primary_key=True, autoincrement=True
    )
    address: Mapped[str] = mapped_column("address", String(), nullable=False)
    type: Mapped[str] = mapped_column("type", String(), nullable=False)


class Office(Base):
    __tablename__ = "office"
    id: Mapped[int] = mapped_column(
        "id", Integer(), primary_key=True, autoincrement=True
    )
    occupation: Mapped[str] = mapped_column(
        "occupation", String(), nullable=False
    )
    name: Mapped[str] = mapped_column("name", String(), nullable=False)
    tg_nickname: Mapped[str] = mapped_column(
        "tg_nickname", String(), nullable=True
    )
    phone: Mapped[str] = mapped_column("phone", String(), nullable=True)
    schedule: Mapped[str] = mapped_column("schedule", String(), nullable=True)
    description: Mapped[str] = mapped_column(
        "description", String(), nullable=True
    )
