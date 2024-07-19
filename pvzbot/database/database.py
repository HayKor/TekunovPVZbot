from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from .models import Base, Users


async def create_all(engine: AsyncEngine) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def create_user(
    async_session: async_sessionmaker[AsyncSession], id, nickname
) -> None:
    async with async_session() as session:
        async with session.begin():
            session.add(
                Users(
                    id=id,
                    nickname=nickname,
                    is_admin=False,
                    is_father=False,
                )
            )


async def make_user_admin(
    async_session: async_sessionmaker[AsyncSession],
    user_id,
) -> None:
    pass
