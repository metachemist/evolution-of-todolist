from pydantic import BaseModel
from typing import Optional


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
    id: str  # Using string to accommodate UUID
    title: str
    description: Optional[str]
    is_completed: bool
    created_at: str  # Using string for datetime
    updated_at: str  # Using string for datetime
    owner_id: str  # Using string to accommodate UUID


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
    id: str  # Using string to accommodate UUID
    email: str
    created_at: str  # Using string for datetime
    updated_at: str  # Using string for datetime