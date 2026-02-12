from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import Index


class User(SQLModel, table=True):
    """
    User model representing a registered user of the system.
    """
    __table_args__ = (
        Index('idx_user_email', 'email'),  # Index on frequently queried field
        Index('idx_user_created_at', 'created_at'),  # Index on frequently queried field
    )
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(max_length=255)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)