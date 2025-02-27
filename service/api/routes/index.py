from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

index_router = APIRouter()

# Redireciona a rota raiz (/) para a documentação Swagger (/docs)
@index_router.get("/", include_in_schema=False)
async def root(request: Request):
    base_url = request.base_url._url.rstrip("/")  # Garante que a URL base seja obtida corretamente
    return RedirectResponse(url=f"{base_url}/docs")
