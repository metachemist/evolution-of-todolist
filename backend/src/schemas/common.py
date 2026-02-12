from pydantic import BaseModel
from typing import Optional


class ErrorResponse(BaseModel):
    """
    Schema for structured error responses.
    """
    success: bool
    data: Optional[object]
    error: dict