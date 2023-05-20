import os

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

__credentional = {
    'db': os.getenv('POSTGRES_DB'),
    'user': os.getenv('POSTGRES_USER'),
    'pswd': os.getenv('POSTGRES_PASSWORD'),
    'host': os.getenv('POSTGRES_HOST'),
    'post': 5432,
}

engine = create_async_engine('postgresql+asyncpg://{user}:{pswd}@{host}:{post}/{db}'.format(**__credentional), echo=False)
async_session = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)
