from fastapi import APIRouter
from fastapi.responses import RedirectResponse

index_router = APIRouter()

# Redireciona a rota raiz (/) para a documentação Swagger (/docs)
@index_router.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")