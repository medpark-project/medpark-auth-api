from contextlib import asynccontextmanager

from fastapi import FastAPI
from src.db.session import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


def create_app() -> FastAPI:
    app = FastAPI(title="MedPark Auth API", version="0.1.0", lifespan=lifespan)
    return app


app = create_app()
