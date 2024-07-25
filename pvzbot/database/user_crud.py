from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from .models import Users


async def get_user_by_id(
    async_session: async_sessionmaker[AsyncSession],
    user_id: int,
) -> Users | None:
    async with async_session() as session:
        user = await session.get(Users, user_id)
    return user


async def get_user_by_nickname(
    async_session: async_sessionmaker[AsyncSession],
    user_nickname: str,
) -> Users | None:
    async with async_session() as session:
        stmt = select(Users).where(Users.nickname == user_nickname)
        user_list = await session.execute(statement=stmt)
        user = user_list.scalar_one_or_none()
    return user


async def create_user(
    async_session: async_sessionmaker[AsyncSession], id: int, nickname: str
) -> Users | None:
    async with async_session() as session:
        check = await get_user_by_id(async_session, id)
        if not check:
            user = Users(id=id, nickname=nickname)
            session.add(user)
            await session.commit()
            return user


async def get_admin_list(
    async_session: async_sessionmaker[AsyncSession],
) -> Sequence[Users] | None:
    async with async_session() as session:
        # stmt = select(Users).where(Users.is_admin == True)
        stmt = select(Users).where(Users.is_admin)
        admin_list = await session.scalars(statement=stmt)
        admin_list = admin_list.all()
    return admin_list


async def make_user_admin(
    async_session: async_sessionmaker[AsyncSession],
    user_id: int,
) -> Users | None:
    async with async_session() as session:
        user = await session.get(Users, user_id)
        if user:
            user.is_admin = True
        await session.commit()
        return user


async def make_user_not_admin(
    async_session: async_sessionmaker[AsyncSession],
    user_id: int,
) -> Users | None:
    async with async_session() as session:
        user = await session.get(Users, user_id)
        if user:
            user.is_admin = False
        await session.commit()
        return user
