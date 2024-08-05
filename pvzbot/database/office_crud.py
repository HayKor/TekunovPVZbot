from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from .models import Office


async def get_office_thing(
    async_session: async_sessionmaker[AsyncSession],
    name: str,
) -> Office | None:
    async with async_session() as session:
        query = select(Office).where(Office.name == name)
        office_obj = await session.execute(query)
        office = office_obj.scalar_one_or_none()
    return office


async def get_office_thing_by_occ_and_name(
    async_session: async_sessionmaker[AsyncSession],
    name: str,
    occupation: str,
) -> Sequence[Office] | None:
    async with async_session() as session:
        query = select(Office).where(
            Office.name == name, Office.occupation == occupation
        )
        office_obj = await session.execute(query)
        office = office_obj.scalars().all()
    return office


async def get_office_thing_all_params(
    async_session: async_sessionmaker[AsyncSession],
    name: str,
    occupation: str,
    tg_nickname: str,
    phone: str,
    schedule: str,
    description: str,
) -> Office | None:
    async with async_session() as session:
        query = select(Office).where(
            Office.name == name,
            Office.occupation == occupation,
            Office.tg_nickname == tg_nickname,
            Office.phone == phone,
            Office.schedule == schedule,
            Office.description == description,
        )
        office_obj = await session.execute(query)
        office = office_obj.scalar_one_or_none()
    return office


async def get_office_thing_by_occupation(
    async_session: async_sessionmaker[AsyncSession],
    occupation: str,
) -> Sequence[Office] | None:
    async with async_session() as session:
        query = select(Office).where(Office.occupation == occupation)
        office_obj = await session.execute(query)
        office = office_obj.scalars()
    return office.all()


async def create_office_thing(
    async_session: async_sessionmaker[AsyncSession],
    name: str,
    occupation: str,
    tg_nickname: str | None = None,
    phone: str | None = None,
    schedule: str | None = None,
    description: str | None = None,
) -> Office | None:
    async with async_session() as session:
        check = await get_office_thing(async_session, name=name)
        if not check:
            office = Office(
                name=name,
                occupation=occupation,
                tg_nickname=tg_nickname,
                phone=phone,
                schedule=schedule,
                description=description,
            )
            session.add(office)
            await session.commit()
            return office


async def delete_office_thing(
    async_session: async_sessionmaker[AsyncSession],
    name: str,
    occupation: str,
    **kwargs,
) -> Sequence[Office] | Office | None:
    async with async_session() as session:
        office_things = await get_office_thing_by_occ_and_name(
            async_session,
            name=name,
            occupation=occupation,
        )
        if office_things:
            for office_thing in office_things:
                await session.delete(office_thing)
        await session.commit()
        return office_things
