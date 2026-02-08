from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone  # <--- Added timezone import

class UserBase(SQLModel):
    # Fixed: Removed sa_type=str
    email: str = Field(unique=True, index=True)
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    # Fixed: Uses lambda for correct UTC time generation
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class UserCreate(UserBase):
    password: str

class UserUpdate(SQLModel):
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)

class UserPublic(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    completed: bool = Field(default=False)

class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    # Fixed: Uses lambda for correct UTC time generation
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class TaskCreate(TaskBase):
    pass

class TaskUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    completed: Optional[bool] = Field(default=None)

class TaskPublic(TaskBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime