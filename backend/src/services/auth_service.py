from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from ..models.user import User
from ..utils.auth import get_password_hash, verify_password


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    """Get a user by their email address."""
    statement = select(User).where(User.email == email)
    result = await db.exec(statement)
    return result.first()


async def create_user(db: AsyncSession, email: str, password: str) -> User:
    """Create a new user with a hashed password."""
    user = User(
        email=email,
        hashed_password=get_password_hash(password),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def authenticate_user(db: AsyncSession, email: str, password: str) -> User | None:
    """Authenticate a user by email and password. Returns the user or None."""
    user = await get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
