from typing import AsyncGenerator
import os
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base
from app.core.config import settings

# Database URL fallback handling for local development without PostgreSQL running
db_url = settings.DATABASE_URL

# Test if sqlite fallback is requested or if default postgres url is used in dev
if settings.ENVIRONMENT != "production" and "postgresql" in db_url:
    # Use SQLite for standalone zero-dependency localhost execution
    sqlite_path = os.path.join(os.getcwd(), "mlcloudengine_local.db")
    db_url = f"sqlite+aiosqlite:///{sqlite_path}"

connect_args = {"check_same_thread": False} if "sqlite" in db_url else {}

# Async SQLAlchemy Engine
engine = create_async_engine(
    db_url,
    echo=False,
    future=True,
    connect_args=connect_args,
)

# Async Session Factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Declarative Base Model
Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to provide Async SQLAlchemy database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
