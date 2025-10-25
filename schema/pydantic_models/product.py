from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, computed_field, AfterValidator, Field


class NewProductSch(BaseModel):
    name: str
    category_id: int = Field(alias="categoryId")
    stock_quantity: Optional[int] = Field(default=1, ge=0, alias="stockQuantity")
