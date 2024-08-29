from config import config
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


engine = create_async_engine(
    url=config.database_url,
    echo=config.engine_echo,
)
async_session = async_sessionmaker(
    engine,
    expire_on_commit=False,
)
