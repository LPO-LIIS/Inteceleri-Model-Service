from pydantic import BaseModel

class ItemCreate(BaseModel):
    name: str
    description: str = None
    price: float
    in_stock: bool = True

class ItemResponse(BaseModel):
    id: str
    name: str
    description: str
    price: float
    in_stock: bool
