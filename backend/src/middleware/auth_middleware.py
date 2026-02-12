from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from typing import Optional
import jwt
import os


class AuthMiddleware:
    """
    Authentication middleware to intercept requests to protected endpoints.
    """
    def __init__(self):
        self.secret_key = os.getenv("SECRET_KEY", "your-default-secret-key-change-in-production")
        self.algorithm = "HS256"

    async def __call__(self, request: Request, call_next):
        # Define public endpoints that don't require authentication
        public_endpoints = ["/", "/health", "/docs", "/redoc", "/openapi.json"]
        
        # Skip authentication for public endpoints
        if request.url.path in public_endpoints:
            response = await call_next(request)
            return response
        
        # Extract token from Authorization header
        authorization = request.headers.get("Authorization")
        if not authorization:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Authorization header is missing"}
            )
        
        if not authorization.startswith("Bearer "):
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid token format. Expected 'Bearer <token>'"}
            )
        
        token = authorization[7:]  # Remove "Bearer " prefix
        
        try:
            # Decode and validate the JWT token
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            user_id = payload.get("sub")
            
            if user_id is None:
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Could not validate credentials"}
                )
            
            # Attach user context to request
            request.state.user_id = user_id
            
        except jwt.ExpiredSignatureError:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Token has expired"}
            )
        except jwt.JWTError:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Could not validate credentials"}
            )
        
        response = await call_next(request)
        return response


# Function to get current user ID from request state
async def get_current_user_id_from_request(request: Request) -> str:
    """
    Get the current user ID from the request state (set by middleware).
    """
    user_id = getattr(request.state, 'user_id', None)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found in request state"
        )
    return user_id