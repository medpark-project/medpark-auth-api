from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.auth.router import router as auth_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="MedPark Auth API",
        version="0.1.0",
        description="Serviço especializado em autenticação e geração de tokens.",
    )

    origins = [
        "http://localhost",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
    return app


app = create_app()
