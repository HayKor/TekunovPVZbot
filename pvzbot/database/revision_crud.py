from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from .models import Revisions


async def get_revision(
    async_session: async_sessionmaker[AsyncSession], id: int
) -> Revisions | None:
    async with async_session() as session:
        query = select(Revisions).where(Revisions.id == id)
        revision_obj = await session.execute(query)
        revision = revision_obj.scalar_one_or_none()
    return revision


async def get_latest_revision(
    async_session: async_sessionmaker[AsyncSession],
) -> Revisions | None:
    async with async_session() as session:
        query = select(Revisions).order_by(Revisions.id.desc()).limit(1)
        revision_obj = await session.execute(query)
        revision = revision_obj.scalar_one_or_none()
    return revision


async def create_revision(
    async_session: async_sessionmaker[AsyncSession],
) -> Revisions | None:
    async with async_session() as session:
        revision = Revisions()
        session.add(revision)
        await session.commit()
        return revision
