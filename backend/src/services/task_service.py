from sqlmodel import select, func
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List, Optional
from uuid import UUID
from ..models.task import Task
from ..models.user import User
from ..schemas.task import TaskCreate, TaskUpdate


async def create_task(db: AsyncSession, user_id: str, title: str, description: str | None) -> Task:
    """
    Create a new task for the specified user.
    """
    task = Task(
        title=title,
        description=description,
        owner_id=UUID(user_id)
    )
    
    db.add(task)
    await db.commit()
    await db.refresh(task)
    
    return task


async def get_tasks(db: AsyncSession, user_id: str) -> List[Task]:
    """
    Get all tasks for the specified user.
    """
    statement = select(Task).where(Task.owner_id == UUID(user_id))
    result = await db.exec(statement)
    return result.all()


async def get_task_by_id(db: AsyncSession, user_id: str, task_id: str) -> Task | None:
    """
    Get a specific task by its ID for the specified user.
    """
    statement = select(Task).where(
        Task.id == UUID(task_id),
        Task.owner_id == UUID(user_id)
    )
    result = await db.exec(statement)
    return result.first()


async def update_task(
    db: AsyncSession, 
    user_id: str, 
    task_id: str, 
    title: str, 
    description: str | None
) -> Task | None:
    """
    Update a specific task for the specified user.
    """
    statement = select(Task).where(
        Task.id == UUID(task_id),
        Task.owner_id == UUID(user_id)
    )
    result = await db.exec(statement)
    task = result.first()
    
    if not task:
        return None
    
    task.title = title
    task.description = description
    task.updated_at = func.now()
    
    await db.commit()
    await db.refresh(task)
    
    return task


async def delete_task(db: AsyncSession, user_id: str, task_id: str) -> bool:
    """
    Delete a specific task for the specified user.
    """
    statement = select(Task).where(
        Task.id == UUID(task_id),
        Task.owner_id == UUID(user_id)
    )
    result = await db.exec(statement)
    task = result.first()
    
    if not task:
        return False
    
    await db.delete(task)
    await db.commit()
    
    return True


async def toggle_completion(db: AsyncSession, user_id: str, task_id: str) -> Task | None:
    """
    Toggle the completion status of a specific task for the specified user.
    """
    statement = select(Task).where(
        Task.id == UUID(task_id),
        Task.owner_id == UUID(user_id)
    )
    result = await db.exec(statement)
    task = result.first()
    
    if not task:
        return None
    
    task.is_completed = not task.is_completed
    task.updated_at = func.now()
    
    await db.commit()
    await db.refresh(task)
    
    return task