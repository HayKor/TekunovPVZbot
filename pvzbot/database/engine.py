from config import config
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


engine = create_async_engine(
    url=config.database_url,
    echo=True,
)
async_session = async_sessionmaker(engine)
