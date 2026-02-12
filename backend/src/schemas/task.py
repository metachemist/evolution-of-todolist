from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID


class TaskCreate(BaseModel):
    """
    Schema for creating new tasks.
    """
    title: str
    description: Optional[str] = None


class TaskUpdate(BaseModel):
    """
    Schema for updating existing tasks.
    """
    title: Optional[str] = None
    description: Optional[str] = None


class TaskResponse(BaseModel):
    """
    Schema for returning task data.
    """
    id: UUID
    title: str
    description: Optional[str]
    is_completed: bool
    created_at: datetime
    updated_at: datetime
    owner_id: UUID


class ErrorResponse(BaseModel):
    """
    Schema for structured error responses.
    """
    success: bool
    data: Optional[object]
    error: dict


class UserResponse(BaseModel):
    """
    Schema for returning user data.
    """
    id: UUID
    email: str
    created_at: datetime
    updated_at: datetime