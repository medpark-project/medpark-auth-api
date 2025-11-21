import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from src import security

router = APIRouter()

MEDPARK_BACKEND_URL = "http://backend:8000"

@router.post("/token", response_model=security.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends()
):

    backend_url = MEDPARK_BACKEND_URL.rstrip("/")
    validate_url = f"{backend_url}/usuarios/auth/validate"
    
    print(f"🔍 TENTATIVA DE CONEXÃO: Conectando em {validate_url}") # LOG 1

    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.post(
                validate_url,
                data={"username": form_data.username, "password": form_data.password}
            )
            response.raise_for_status()
        
        except httpx.HTTPStatusError as e:
            print(f"⚠️ RESPOSTA DE ERRO DO BACKEND: {e.response.status_code} - {e.response.text}") # LOG 2
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="E-mail ou senha incorretos",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except httpx.RequestError as e:
            print(f"❌ FALHA CRÍTICA DE CONEXÃO: {str(e)}") # LOG 3
            print(f"❌ TIPO DO ERRO: {type(e)}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Falha de comunicação com Backend: {str(e)}",
            )
            
    user_data = response.json()
    access_token = security.create_access_token(
        data={"sub": user_data["email"], "profile": user_data["profile"]}
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

"""
@router.post("/token", response_model=security.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    validate_url = f"{MEDPARK_BACKEND_URL}/usuarios/auth/validate"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                validate_url,
                data={"username": form_data.username, "password": form_data.password},
            )
            response.raise_for_status()

        except httpx.HTTPStatusError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="E-mail ou senha incorretos",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except httpx.RequestError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Serviço de validação de usuário indisponível.",
            )

    user_data = response.json()

    access_token = security.create_access_token(
        data={"sub": user_data["email"], "profile": user_data["profile"]}
    )

    return {"access_token": access_token, "token_type": "bearer"}


"""
