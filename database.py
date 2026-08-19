import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

# Load variables from .env into the environment
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# The engine manages the actual connection pool to Postgres
engine = create_async_engine(DATABASE_URL, echo=True)

# session_maker creates new "conversations" with the database for each request
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

# Base class that all our database models (tables) will inherit from
Base = declarative_base()

# Dependency function FastAPI will use to give each request its own DB session
async def get_db():
    async with async_session_maker() as session:
        yield session