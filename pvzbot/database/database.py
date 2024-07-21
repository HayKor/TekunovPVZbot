from sqlalchemy.ext.asyncio import AsyncEngine

from .models import Base


async def create_all(engine: AsyncEngine) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
