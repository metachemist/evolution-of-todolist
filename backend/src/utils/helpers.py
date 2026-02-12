from typing import Any, Optional
from fastapi import HTTPException, status
from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """
    Standard error response format.
    """
    success: bool = False
    data: Optional[Any] = None
    error: dict


def create_error_response(code: str, message: str, details: Optional[dict] = None) -> ErrorResponse:
    """
    Create a standardized error response.
    """
    error_obj = {
        "code": code,
        "message": message
    }
    
    if details:
        error_obj["details"] = details
    
    return ErrorResponse(success=False, data=None, error=error_obj)


def raise_http_exception(status_code: int, detail: str, headers: Optional[dict] = None):
    """
    Raise an HTTP exception with the specified status code and detail.
    """
    raise HTTPException(status_code=status_code, detail=detail, headers=headers)


def handle_error_and_raise(status_code: int, error_code: str, message: str):
    """
    Create an error response and raise an HTTP exception.
    """
    error_response = create_error_response(error_code, message)
    raise HTTPException(status_code=status_code, detail=error_response.dict())