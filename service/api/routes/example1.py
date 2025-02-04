from fastapi import APIRouter, HTTPException, Request, status
from api.database import parse_obj_id
from api.models import ItemModel
from api.schemas import ItemCreate, ItemResponse
from bson import ObjectId

example1_router = APIRouter()


@example1_router.post(
    "/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED
)
async def create_item(item: ItemCreate, request: Request):
    if request.app.state.db is None:
        raise HTTPException(status_code=500, detail="Database connection not available")
    item_data = item.dict()
    result = await request.app.state.db["items"].insert_one(item_data)
    item_data["_id"] = result.inserted_id
    return parse_obj_id(item_data)


@example1_router.get("/", response_model=list[ItemResponse])
async def list_items(request: Request):
    items = await request.app.state.db["items"].find().to_list(100)
    return [parse_obj_id(item) for item in items]
