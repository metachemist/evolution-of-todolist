from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List
from uuid import UUID
from ..database import get_db_session
from ..services.task_service import (
    get_tasks, create_task, get_task_by_id, update_task, 
    delete_task, toggle_completion
)
from ..services.user_service import get_user_by_id
from ..utils.auth import get_current_user_id
from ..utils.helpers import create_error_response
from ..schemas.task import TaskCreate, TaskUpdate, TaskResponse


router = APIRouter(prefix="/api/{user_id}", tags=["tasks"])


@router.get("/tasks", response_model=List[TaskResponse])
async def get_user_tasks(
    user_id: str,
    current_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Retrieve all tasks for the specified user.
    """
    # Verify that the user_id in the path matches the authenticated user
    if user_id != current_user_id:
        error_response = create_error_response(
            code="UNAUTHORIZED_ACCESS",
            message="You can only access your own tasks"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=error_response.dict()
        )
    
    # Verify the user exists
    user = await get_user_by_id(db, user_id)
    if not user:
        error_response = create_error_response(
            code="USER_NOT_FOUND",
            message=f"User with id {user_id} not found"
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_response.dict()
        )
    
    tasks = await get_tasks(db, user_id)
    return tasks


@router.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_user_task(
    user_id: str,
    task_data: TaskCreate,
    current_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Create a new task for the specified user.
    """
    # Verify that the user_id in the path matches the authenticated user
    if user_id != current_user_id:
        error_response = create_error_response(
            code="UNAUTHORIZED_ACCESS",
            message="You can only create tasks for yourself"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=error_response.dict()
        )
    
    # Verify the user exists
    user = await get_user_by_id(db, user_id)
    if not user:
        error_response = create_error_response(
            code="USER_NOT_FOUND",
            message=f"User with id {user_id} not found"
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_response.dict()
        )
    
    # Create the task
    task = await create_task(
        db, 
        user_id, 
        task_data.title, 
        task_data.description
    )
    
    return task


@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_specific_task(
    user_id: str,
    task_id: str,  # Using string to accommodate UUID
    current_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Retrieve a specific task for the specified user.
    """
    # Verify that the user_id in the path matches the authenticated user
    if user_id != current_user_id:
        error_response = create_error_response(
            code="UNAUTHORIZED_ACCESS",
            message="You can only access your own tasks"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=error_response.dict()
        )
    
    # Verify the user exists
    user = await get_user_by_id(db, user_id)
    if not user:
        error_response = create_error_response(
            code="USER_NOT_FOUND",
            message=f"User with id {user_id} not found"
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_response.dict()
        )
    
    # Get the specific task
    task = await get_task_by_id(db, user_id, task_id)
    if not task:
        error_response = create_error_response(
            code="TASK_NOT_FOUND",
            message=f"Task with id {task_id} not found for user {user_id}"
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_response.dict()
        )
    
    return task


@router.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_user_task(
    user_id: str,
    task_id: str,  # Using string to accommodate UUID
    task_data: TaskUpdate,
    current_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Update a specific task for the specified user.
    """
    # Verify that the user_id in the path matches the authenticated user
    if user_id != current_user_id:
        error_response = create_error_response(
            code="UNAUTHORIZED_ACCESS",
            message="You can only update your own tasks"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=error_response.dict()
        )
    
    # Verify the user exists
    user = await get_user_by_id(db, user_id)
    if not user:
        error_response = create_error_response(
            code="USER_NOT_FOUND",
            message=f"User with id {user_id} not found"
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_response.dict()
        )
    
    # Update the task
    updated_task = await update_task(
        db, 
        user_id, 
        task_id, 
        task_data.title or "",  # Provide default if None
        task_data.description
    )
    
    if not updated_task:
        error_response = create_error_response(
            code="TASK_NOT_FOUND",
            message=f"Task with id {task_id} not found for user {user_id}"
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_response.dict()
        )
    
    return updated_task


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_task(
    user_id: str,
    task_id: str,  # Using string to accommodate UUID
    current_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Delete a specific task for the specified user.
    """
    # Verify that the user_id in the path matches the authenticated user
    if user_id != current_user_id:
        error_response = create_error_response(
            code="UNAUTHORIZED_ACCESS",
            message="You can only delete your own tasks"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=error_response.dict()
        )
    
    # Verify the user exists
    user = await get_user_by_id(db, user_id)
    if not user:
        error_response = create_error_response(
            code="USER_NOT_FOUND",
            message=f"User with id {user_id} not found"
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_response.dict()
        )
    
    # Delete the task
    success = await delete_task(db, user_id, task_id)
    
    if not success:
        error_response = create_error_response(
            code="TASK_NOT_FOUND",
            message=f"Task with id {task_id} not found for user {user_id}"
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_response.dict()
        )
    
    return


@router.patch("/tasks/{task_id}/complete", response_model=TaskResponse)
async def toggle_task_completion(
    user_id: str,
    task_id: str,  # Using string to accommodate UUID
    current_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Toggle the completion status of a specific task for the specified user.
    """
    # Verify that the user_id in the path matches the authenticated user
    if user_id != current_user_id:
        error_response = create_error_response(
            code="UNAUTHORIZED_ACCESS",
            message="You can only update your own tasks"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=error_response.dict()
        )
    
    # Verify the user exists
    user = await get_user_by_id(db, user_id)
    if not user:
        error_response = create_error_response(
            code="USER_NOT_FOUND",
            message=f"User with id {user_id} not found"
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_response.dict()
        )
    
    # Toggle the task completion
    updated_task = await toggle_completion(db, user_id, task_id)
    
    if not updated_task:
        error_response = create_error_response(
            code="TASK_NOT_FOUND",
            message=f"Task with id {task_id} not found for user {user_id}"
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_response.dict()
        )
    
    return updated_task