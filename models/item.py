from pydantic import BaseModel, Field
from ..models.category import Category

class Item(BaseModel):
    name: str
    price: float
    count: int
    id: int
    category: Category

class ItemV1(BaseModel):
    name: str = Field(description="Name of the item.")
    price: float = Field(default=0.0,description="Price of the item.")
    count: int = Field(default=0,description="Amount of instances of this item in stock")
    id: int = Field(description="Unique integer that specifies this item.")
    category: Category = Field(description="Category this item belongs to.")