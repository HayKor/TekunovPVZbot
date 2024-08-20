from datetime import date as dat

from sqlalchemy import Date, ForeignKey, func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(AsyncAttrs, DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


class Users(Base):
    __tablename__ = "users"
    nickname: Mapped[str]
    is_admin: Mapped[bool] = mapped_column(default=False)
    is_father: Mapped[bool] = mapped_column(default=False)


class Points(Base):
    __tablename__ = "points"
    address: Mapped[str]
    type: Mapped[str]


class Office(Base):
    __tablename__ = "office"
    occupation: Mapped[str]
    name: Mapped[str]

    # Optional fields
    tg_nickname: Mapped[str | None]
    phone: Mapped[str | None]
    schedule: Mapped[str | None]
    description: Mapped[str | None]


class Revisions(Base):
    __tablename__ = "revisions"
    date: Mapped[dat] = mapped_column(Date(), default=func.current_date())

    # relationships
    polls: Mapped[list["Polls"]] = relationship(
        "Polls", back_populates="revision", lazy="selectin"
    )


class Polls(Base):
    __tablename__ = "polls"
    revision_id: Mapped[int] = mapped_column(
        ForeignKey("revisions.id"), default=-1
    )

    # relationships
    poll_answers: Mapped[list["PollAnswers"]] = relationship(
        "PollAnswers", back_populates="poll", lazy="selectin"
    )
    revision: Mapped["Revisions"] = relationship(
        "Revisions", back_populates="polls", lazy="selectin"
    )


class PollAnswers(Base):
    __tablename__ = "poll_answers"
    poll_id: Mapped[int] = mapped_column(ForeignKey("polls.id"))
    question: Mapped[str]
    option_id: Mapped[int]
    is_answered: Mapped[bool] = mapped_column(default=False)

    # relationships
    poll: Mapped["Polls"] = relationship(
        "Polls", back_populates="poll_answers", lazy="selectin"
    )
