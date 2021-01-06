from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

class DateTimeModelMixin(BaseModel):
    created_at: Optional[datetime] = Field(...)
    updated_at: Optional[datetime] = Field(...)

class DBModelMixin(DateTimeModelMixin):
    id: Optional[int] = None