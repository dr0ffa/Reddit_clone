from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from contextlib import asynccontextmanager

DATABASE_URL = "postgresql+asyncpg://user:password@db:5432/auth-db"

engine = create_async_engine(DATABASE_URL, echo=True, future=True)

AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
)

Base = declarative_base()

@asynccontextmanager
async def get_db_context():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except:
            await session.rollback()
            raise