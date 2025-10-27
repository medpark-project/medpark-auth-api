from fastapi import FastAPI
from src.auth.router import router as auth_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="MedPark Auth API",
        version="0.1.0",
        description="Serviço especializado em autenticação e geração de tokens.",
    )
    app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
    return app


app = create_app()
