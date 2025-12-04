from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.db_context import auto_create_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Provides a context manager for managing the lifespan of a FastAPI application.
    """

    auto_create_db()

    yield
