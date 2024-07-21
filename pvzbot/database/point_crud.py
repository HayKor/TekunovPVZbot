from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from .models import Points


async def get_point(
    async_session: async_sessionmaker[AsyncSession],
    address: str,
    type: str,
) -> Points | None:
    async with async_session() as session:
        query = select(Points).where(Points.address == address, Points.type == type)
        point_obj = await session.execute(query)
        point = point_obj.scalar_one_or_none()
    return point


async def get_points(
    async_session: async_sessionmaker[AsyncSession],
) -> Sequence[Points] | None:
    async with async_session() as session:
        stmt = select(Points).order_by(Points.address, Points.type)
        points_obj = await session.scalars(statement=stmt)
        points = points_obj.all()
    return points


async def create_point(
    async_session: async_sessionmaker[AsyncSession], address, type
) -> Points | None:
    async with async_session() as session:
        check = await get_point(async_session, address, type)
        if not check:
            point = Points(address=address, type=type)
            session.add(point)
            await session.commit()
            return point
