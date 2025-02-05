from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

index_router = APIRouter()

# Redireciona a rota raiz (/) para a documentação Swagger (/docs)
@index_router.get("/", include_in_schema=False)
async def root(request: Request):
    return RedirectResponse(url=request.scope.get("root_path", "") + "/docs")