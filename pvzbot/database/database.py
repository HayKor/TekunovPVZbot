from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from .models import Base, Users


async def create_all(engine: AsyncEngine) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_user_by_id(
    async_session: async_sessionmaker[AsyncSession],
    user_id,
) -> Users | None:
    async with async_session() as session:
        user = await session.get(Users, user_id)
    return user


async def create_user(
    async_session: async_sessionmaker[AsyncSession], id, nickname
) -> Users | None:
    async with async_session() as session:
        async with session.begin():
            user = await session.get(Users, id)
            if not user:
                session.add(
                    Users(
                        id=id,
                        nickname=nickname,
                        is_admin=False,
                        is_father=False,
                    )
                )
            return user


async def make_user_admin(
    async_session: async_sessionmaker[AsyncSession],
    user_id,
) -> Users | None:
    async with async_session() as session:
        user = await session.get(Users, user_id)
        if user:
            user.is_admin = True
        await session.commit()
        return user
