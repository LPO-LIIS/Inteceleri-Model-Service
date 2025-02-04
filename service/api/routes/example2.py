from fastapi import APIRouter, HTTPException, Request, status
from api.database import parse_obj_id
from api.models import ItemModel
from api.schemas import ItemCreate, ItemResponse
from bson import ObjectId

example2_router = APIRouter()


@example2_router.get("/{item_id}", response_model=ItemResponse)
async def get_item(item_id: str, request: Request):
    if not ObjectId.is_valid(item_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID")
    item = await request.app.state.db["items"].find_one({"_id": ObjectId(item_id)})
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return parse_obj_id(item)

@example2_router.put("/{item_id}", response_model=ItemResponse)
async def update_item(item_id: str, item: ItemCreate, request: Request):
    if not ObjectId.is_valid(item_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID")
    result = await request.app.state.db["items"].update_one({"_id": ObjectId(item_id)}, {"$set": item.dict()})
    if result.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    updated_item = await request.app.state.db["items"].find_one({"_id": ObjectId(item_id)})
    return parse_obj_id(updated_item)

@example2_router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: str, request: Request):
    if not ObjectId.is_valid(item_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID")
    result = await request.app.state.db["items"].delete_one({"_id": ObjectId(item_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
