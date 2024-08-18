from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from .models import PollAnswers, Polls


async def get_poll(
    async_session: async_sessionmaker[AsyncSession], poll_id: int
) -> Polls | None:
    async with async_session() as session:
        query = select(Polls).where(Polls.id == poll_id)
        poll_obj = await session.execute(query)
        poll = poll_obj.scalar_one_or_none()
    return poll


async def create_poll(
    async_session: async_sessionmaker[AsyncSession], poll_id: int
) -> Polls | None:
    async with async_session() as session:
        check = await get_poll(async_session, poll_id)
        if not check:
            poll = Polls(
                id=poll_id,
            )
            session.add(poll)
            await session.commit()
            return poll


async def update_revision_id(
    async_session: async_sessionmaker[AsyncSession],
    poll_id: int,
    revision_id: int,
) -> Polls | None:
    async with async_session() as session:
        poll = await get_poll(async_session, poll_id)
        if poll:
            poll = await session.get(Polls, poll.id)
            poll.revision_id = revision_id
        await session.commit()
        return poll


async def get_poll_answer(
    async_session: async_sessionmaker[AsyncSession],
    poll_id: int,
    option_id: int,
) -> PollAnswers | None:
    async with async_session() as session:
        query = select(PollAnswers).where(
            PollAnswers.poll_id == poll_id,
            PollAnswers.option_id == option_id,
        )
        poll_answer_obj = await session.execute(query)
        poll_answer = poll_answer_obj.scalar_one_or_none()
    return poll_answer


async def create_poll_answer(
    async_session: async_sessionmaker[AsyncSession],
    poll_id: int,
    question: str,
    option_id: int,
) -> PollAnswers | None:
    async with async_session() as session:
        check = await get_poll_answer(async_session, poll_id, option_id)
        if not check:
            poll_answer = PollAnswers(
                poll_id=poll_id,
                question=question,
                option_id=option_id,
            )
            session.add(poll_answer)
            await session.commit()
            return poll_answer


async def update_poll_answer_true(
    async_session: async_sessionmaker[AsyncSession],
    poll_id: int,
    option_id: int,
) -> PollAnswers | None:
    async with async_session() as session:
        poll_answer = await get_poll_answer(async_session, poll_id, option_id)
        if poll_answer:
            poll_answer = await session.get(PollAnswers, poll_answer.id)
            poll_answer.is_answered = True
        await session.commit()
        return poll_answer
