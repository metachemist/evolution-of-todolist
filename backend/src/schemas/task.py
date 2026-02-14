from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID


class TaskCreate(BaseModel):
    """Schema for creating new tasks."""
    title: str
    description: Optional[str] = None


class TaskUpdate(BaseModel):
    """Schema for updating existing tasks."""
    title: Optional[str] = None
    description: Optional[str] = None


class TaskResponse(BaseModel):
    """Schema for returning task data."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    description: Optional[str]
    is_completed: bool
    created_at: datetime
    updated_at: datetime
    owner_id: UUID
