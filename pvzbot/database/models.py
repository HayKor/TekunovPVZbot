from datetime import date, datetime, timezone

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(AsyncAttrs, DeclarativeBase):
    id: Mapped[int] = mapped_column(
        "id", Integer(), primary_key=True, autoincrement=True
    )


class Users(Base):
    __tablename__ = "users"
    nickname: Mapped[str] = mapped_column("nickname", nullable=False)
    is_admin: Mapped[bool] = mapped_column("is_admin", default=False)
    is_father: Mapped[bool] = mapped_column("is_father", default=False)


class Points(Base):
    __tablename__ = "points"
    address: Mapped[str] = mapped_column("address", nullable=False)
    type: Mapped[str] = mapped_column("type", nullable=False)


class Office(Base):
    __tablename__ = "office"
    occupation: Mapped[str] = mapped_column("occupation", nullable=False)
    name: Mapped[str] = mapped_column("name", nullable=False)
    tg_nickname: Mapped[str] = mapped_column("tg_nickname", nullable=True)
    phone: Mapped[str] = mapped_column("phone", nullable=True)
    schedule: Mapped[str] = mapped_column("schedule", nullable=True)
    description: Mapped[str] = mapped_column("description", nullable=True)


class Polls(Base):
    __tablename__ = "polls"
    # date: Mapped[date] = mapped_column(
    # "date", DateTime(timezone=True), default=datetime.now(timezone.utc)
    # )
    date: Mapped[date] = mapped_column(
        "date", Date(), default=func.current_date()
    )
    poll_answers: Mapped[list["PollAnswers"]] = relationship(
        "PollAnswers", back_populates="polls"
    )


class PollAnswers(Base):
    __tablename__ = "poll_answers"
    poll_id: Mapped[int] = mapped_column("poll_id", ForeignKey("polls.id"))
    question: Mapped[str] = mapped_column("question", nullable=False)
    is_answered: Mapped[bool] = mapped_column("is_answered", default=False)
    poll: Mapped["Polls"] = relationship("Poll", back_populates="poll_answers")
