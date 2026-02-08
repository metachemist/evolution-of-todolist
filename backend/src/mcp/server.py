from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any, Optional
from datetime import datetime
from sqlmodel import Session, select
from ..models import Task, TaskCreate, TaskUpdate, TaskPublic, User, UserCreate
from ..db import get_session
from ..auth import get_current_user, get_password_hash, authenticate_user, create_access_token
from ..auth.auth_handler import verify_password


router = APIRouter(prefix="/mcp/tools", tags=["mcp-tools"])


@router.post("/register_user")
async def mcp_register_user(
    email: str,
    password: str,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    session: Session = Depends(get_session)
) -> Dict[str, Any]:
    """
    MCP tool for registering a new user.

    Args:
        email: The email address for the new user
        password: The password for the new user
        first_name: Optional first name for the user
        last_name: Optional last name for the user
        session: Database session

    Returns:
        Dictionary with success status and user data
    """
    # Validate input
    if not email or "@" not in email:
        raise HTTPException(status_code=400, detail="Valid email is required")

    if len(password) < 8 or len(password) > 20 or not any(c in "!@#$%^&.*" for c in password):
        raise HTTPException(
            status_code=400, 
            detail="Password must be 8-20 characters long and contain at least one special character"
        )

    # Check if user already exists
    existing_user_statement = select(User).where(User.email == email)
    existing_user_result = await session.execute(existing_user_statement)
    existing_user = existing_user_result.first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create new user
    hashed_password = get_password_hash(password)
    user = User(
        email=email,
        hashed_password=hashed_password,
        first_name=first_name,
        last_name=last_name
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    # Generate JWT token
    access_token = create_access_token(data={"sub": user.email})

    # Prepare response
    response_data = {
        "success": True,
        "data": {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "created_at": user.created_at.isoformat(),
            "updated_at": user.updated_at.isoformat(),
            "token": access_token
        },
        "metadata": {
            "tool_name": "register_user",
            "timestamp": datetime.utcnow().isoformat(),
            "execution_time_ms": 0  # Placeholder, actual timing would be measured
        }
    }

    return response_data


@router.post("/authenticate_user")
async def mcp_authenticate_user(
    email: str,
    password: str,
    session: Session = Depends(get_session)
) -> Dict[str, Any]:
    """
    MCP tool for authenticating a user.

    Args:
        email: The email address of the user
        password: The password of the user
        session: Database session

    Returns:
        Dictionary with success status and user data
    """
    # Validate input
    if not email or "@" not in email:
        raise HTTPException(status_code=400, detail="Valid email is required")

    if not password:
        raise HTTPException(status_code=400, detail="Password is required")

    # Look up user by email
    user_statement = select(User).where(User.email == email)
    user_result = await session.execute(user_statement)
    user = user_result.first()

    # Verify user exists and password is correct
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Generate JWT token
    access_token = create_access_token(data={"sub": user.email})

    # Prepare response
    response_data = {
        "success": True,
        "data": {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "created_at": user.created_at.isoformat(),
            "updated_at": user.updated_at.isoformat(),
            "token": access_token
        },
        "metadata": {
            "tool_name": "authenticate_user",
            "timestamp": datetime.utcnow().isoformat(),
            "execution_time_ms": 0  # Placeholder, actual timing would be measured
        }
    }

    return response_data


@router.post("/get_current_user")
async def mcp_get_current_user(
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    MCP tool for retrieving the current authenticated user's information.

    Args:
        current_user: The authenticated user (obtained via JWT token)

    Returns:
        Dictionary with success status and user data
    """
    # Prepare response
    response_data = {
        "success": True,
        "data": {
            "id": current_user.id,
            "email": current_user.email,
            "first_name": current_user.first_name,
            "last_name": current_user.last_name,
            "created_at": current_user.created_at.isoformat(),
            "updated_at": current_user.updated_at.isoformat()
        },
        "metadata": {
            "tool_name": "get_current_user",
            "timestamp": datetime.utcnow().isoformat(),
            "execution_time_ms": 0  # Placeholder, actual timing would be measured
        }
    }

    return response_data


@router.post("/create_task")
async def mcp_create_task(
    user_id: int,
    title: str,
    description: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> Dict[str, Any]:
    """
    MCP tool for creating a new task for the authenticated user.
    
    Args:
        user_id: The ID of the user creating the task
        title: The title of the task
        description: Optional description of the task
        current_user: The authenticated user
        session: Database session
    
    Returns:
        Dictionary with success status and task data
    """
    # Verify that the user_id matches the authenticated user's ID
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Access denied: Cannot create tasks for another user")
    
    # Validate input
    if not title or len(title.strip()) == 0:
        raise HTTPException(status_code=400, detail="Title is required and cannot be empty")
    
    if len(title) > 200:
        raise HTTPException(status_code=400, detail="Title exceeds maximum length of 200 characters")
    
    if description and len(description) > 1000:
        raise HTTPException(status_code=400, detail="Description exceeds maximum length of 1000 characters")
    
    # Create the task
    task = Task(
        title=title.strip(),
        description=description,
        user_id=user_id,
        completed=False
    )
    
    session.add(task)
    await session.commit()
    await session.refresh(task)
    
    # Prepare response
    response_data = {
        "success": True,
        "data": {
            "id": task.id,
            "user_id": task.user_id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat()
        },
        "metadata": {
            "tool_name": "create_task",
            "timestamp": datetime.utcnow().isoformat(),
            "execution_time_ms": 0  # Placeholder, actual timing would be measured
        }
    }
    
    return response_data


@router.post("/get_user_tasks")
async def mcp_get_user_tasks(
    user_id: int,
    limit: int = 20,
    offset: int = 0,
    completed: Optional[bool] = None,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> Dict[str, Any]:
    """
    MCP tool for retrieving all tasks for the specified user.
    
    Args:
        user_id: The ID of the user whose tasks to retrieve
        limit: Number of tasks to return per page (default: 20, max: 100)
        offset: Number of tasks to skip (for pagination, default: 0)
        completed: Filter by completion status (true/false/all, default: None)
        current_user: The authenticated user
        session: Database session
    
    Returns:
        Dictionary with success status and tasks data
    """
    # Verify that the user_id matches the authenticated user's ID
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Access denied: Cannot access another user's tasks")
    
    # Validate parameters
    if limit <= 0 or limit > 100:
        raise HTTPException(status_code=400, detail="Limit must be between 1 and 100")
    
    if offset < 0:
        raise HTTPException(status_code=400, detail="Offset must be greater than or equal to 0")
    
    # Build query
    query = select(Task).where(Task.user_id == user_id)
    
    # Apply completion filter if specified
    if completed is not None:
        query = query.where(Task.completed == completed)
    
    # Apply ordering and pagination
    query = query.order_by(Task.created_at.desc()).offset(offset).limit(limit)
    
    result = await session.execute(query)
    tasks = result.scalars().all()
    
    # Count total tasks for pagination metadata
    count_query = select(Task).where(Task.user_id == user_id)
    if completed is not None:
        count_query = count_query.where(Task.completed == completed)
    
    count_result = await session.execute(count_query)
    total_count = len(count_result.scalars().all())
    
    # Convert tasks to dict format
    tasks_list = []
    for task in tasks:
        tasks_list.append({
            "id": task.id,
            "user_id": task.user_id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat()
        })
    
    # Prepare response
    response_data = {
        "success": True,
        "data": {
            "tasks": tasks_list,
            "pagination": {
                "total": total_count,
                "limit": limit,
                "offset": offset,
                "has_more": (offset + limit) < total_count
            }
        },
        "metadata": {
            "tool_name": "get_user_tasks",
            "timestamp": datetime.utcnow().isoformat(),
            "execution_time_ms": 0  # Placeholder, actual timing would be measured
        }
    }
    
    return response_data


@router.post("/get_task")
async def mcp_get_task(
    user_id: int,
    task_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> Dict[str, Any]:
    """
    MCP tool for retrieving a specific task by ID for the specified user.
    
    Args:
        user_id: The ID of the user who owns the task
        task_id: The ID of the task to retrieve
        current_user: The authenticated user
        session: Database session
    
    Returns:
        Dictionary with success status and task data
    """
    # Verify that the user_id matches the authenticated user's ID
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Access denied: Cannot access another user's tasks")
    
    # Query for the specific task
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    result = await session.execute(statement)
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Prepare response
    response_data = {
        "success": True,
        "data": {
            "id": task.id,
            "user_id": task.user_id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat()
        },
        "metadata": {
            "tool_name": "get_task",
            "timestamp": datetime.utcnow().isoformat(),
            "execution_time_ms": 0  # Placeholder, actual timing would be measured
        }
    }
    
    return response_data


@router.post("/update_task")
async def mcp_update_task(
    user_id: int,
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    completed: Optional[bool] = None,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> Dict[str, Any]:
    """
    MCP tool for updating an existing task for the authenticated user.
    
    Args:
        user_id: The ID of the user who owns the task
        task_id: The ID of the task to update
        title: Optional new title for the task
        description: Optional new description for the task
        completed: Optional new completion status for the task
        current_user: The authenticated user
        session: Database session
    
    Returns:
        Dictionary with success status and updated task data
    """
    # Verify that the user_id matches the authenticated user's ID
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Access denied: Cannot update another user's tasks")
    
    # Query for the specific task
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    result = await session.execute(statement)
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Update the task with the provided data
    if title is not None:
        if len(title.strip()) == 0:
            raise HTTPException(status_code=400, detail="Title cannot be empty")
        
        if len(title) > 200:
            raise HTTPException(status_code=400, detail="Title exceeds maximum length of 200 characters")
        
        task.title = title.strip()
    
    if description is not None:
        if len(description) > 1000:
            raise HTTPException(status_code=400, detail="Description exceeds maximum length of 1000 characters")
        
        task.description = description
    
    if completed is not None:
        task.completed = completed
    
    task.updated_at = datetime.utcnow()
    session.add(task)
    await session.commit()
    await session.refresh(task)
    
    # Prepare response
    response_data = {
        "success": True,
        "data": {
            "id": task.id,
            "user_id": task.user_id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat()
        },
        "metadata": {
            "tool_name": "update_task",
            "timestamp": datetime.utcnow().isoformat(),
            "execution_time_ms": 0  # Placeholder, actual timing would be measured
        }
    }
    
    return response_data


@router.post("/delete_task")
async def mcp_delete_task(
    user_id: int,
    task_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> Dict[str, Any]:
    """
    MCP tool for deleting a specific task for the authenticated user.
    
    Args:
        user_id: The ID of the user who owns the task
        task_id: The ID of the task to delete
        current_user: The authenticated user
        session: Database session
    
    Returns:
        Dictionary with success status and message
    """
    # Verify that the user_id matches the authenticated user's ID
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Access denied: Cannot delete another user's tasks")
    
    # Query for the specific task
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    result = await session.execute(statement)
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    session.delete(task)
    await session.commit()
    
    # Prepare response
    response_data = {
        "success": True,
        "data": {
            "message": "Task deleted successfully"
        },
        "metadata": {
            "tool_name": "delete_task",
            "timestamp": datetime.utcnow().isoformat(),
            "execution_time_ms": 0  # Placeholder, actual timing would be measured
        }
    }
    
    return response_data


@router.post("/toggle_task_completion")
async def mcp_toggle_task_completion(
    user_id: int,
    task_id: int,
    completed: bool,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> Dict[str, Any]:
    """
    MCP tool for toggling or setting the completion status of a task.
    
    Args:
        user_id: The ID of the user who owns the task
        task_id: The ID of the task to update
        completed: The new completion status for the task
        current_user: The authenticated user
        session: Database session
    
    Returns:
        Dictionary with success status and updated task data
    """
    # Verify that the user_id matches the authenticated user's ID
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Access denied: Cannot modify another user's tasks")
    
    # Query for the specific task
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    result = await session.execute(statement)
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Update the completion status
    task.completed = completed
    task.updated_at = datetime.utcnow()
    
    session.add(task)
    await session.commit()
    await session.refresh(task)
    
    # Prepare response
    response_data = {
        "success": True,
        "data": {
            "id": task.id,
            "user_id": task.user_id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat()
        },
        "metadata": {
            "tool_name": "toggle_task_completion",
            "timestamp": datetime.utcnow().isoformat(),
            "execution_time_ms": 0  # Placeholder, actual timing would be measured
        }
    }
    
    return response_data