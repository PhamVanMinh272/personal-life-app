from typing import Optional

from pydantic import BaseModel, Field


class Sort(BaseModel):
    sort_by: Optional[str] = Field(default=None, description="Field to sort by")
    sort_order: Optional[str] = Field(
        default="asc",
        description="Sort order: 'asc' for ascending, 'desc' for descending",
    )