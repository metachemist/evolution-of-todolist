from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from ..database import get_db_session
from ..schemas.user import UserCreate, UserLogin
from ..schemas.common import TokenResponse
from ..services.auth_service import create_user, authenticate_user, get_user_by_email
from ..utils.auth import create_access_token
from ..utils.helpers import create_error_response


router = APIRouter(tags=["auth"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db_session),
):
    """Register a new user and return an access token."""
    existing = await get_user_by_email(db, user_data.email)
    if existing:
        error_response = create_error_response(
            code="EMAIL_ALREADY_EXISTS",
            message="A user with this email already exists",
        )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=error_response.model_dump(),
        )

    user = await create_user(db, user_data.email, user_data.password)
    token = create_access_token(data={"sub": str(user.id)})
    return TokenResponse(access_token=token)


@router.post("/login", response_model=TokenResponse)
async def login(
    user_data: UserLogin,
    db: AsyncSession = Depends(get_db_session),
):
    """Authenticate a user and return an access token."""
    user = await authenticate_user(db, user_data.email, user_data.password)
    if not user:
        error_response = create_error_response(
            code="INVALID_CREDENTIALS",
            message="Invalid email or password",
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error_response.model_dump(),
        )

    token = create_access_token(data={"sub": str(user.id)})
    return TokenResponse(access_token=token)
