from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID


class UserResponse(BaseModel):
    """
    Schema for returning user data.
    """
    id: UUID
    email: str
    created_at: datetime
    updated_at: datetime