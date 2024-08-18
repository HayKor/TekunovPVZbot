from datetime import date as dat

from sqlalchemy import Date, ForeignKey, Integer, func
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


class Revisions(Base):
    __tablename__ = "revisions"
    date: Mapped[dat] = mapped_column(
        "date", Date(), default=func.current_date()
    )

    polls: Mapped[list["Polls"]] = relationship(
        "Polls", back_populates="revision", lazy="selectin"
    )


class Polls(Base):
    __tablename__ = "polls"
    revision_id: Mapped[int] = mapped_column(
        "revision_id", ForeignKey("revisions.id"), default=-1
    )

    poll_answers: Mapped[list["PollAnswers"]] = relationship(
        "PollAnswers", back_populates="poll", lazy="selectin"
    )
    revision: Mapped["Revisions"] = relationship(
        "Revisions", back_populates="polls", lazy="selectin"
    )


class PollAnswers(Base):
    __tablename__ = "poll_answers"
    poll_id: Mapped[int] = mapped_column("poll_id", ForeignKey("polls.id"))
    question: Mapped[str] = mapped_column("question", nullable=False)
    option_id: Mapped[int] = mapped_column("option_id", nullable=False)
    is_answered: Mapped[bool] = mapped_column("is_answered", default=False)

    poll: Mapped["Polls"] = relationship(
        "Polls", back_populates="poll_answers", lazy="selectin"
    )
