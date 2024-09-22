#!/usr/bin/env python
"""FastAPI router related to group1."""
from fastapi import APIRouter
from schemas import TaskId
from . import tasks
from . import schemas

router = APIRouter()


@router.post("/request-add")
async def send_add_task(a: int, b: int) -> TaskId:
    """Send a task to add two numbers.

    This function sends a task to the Celery worker to add two numbers. It
    returns the task ID to the client.

    Args:
        a (int): The first number.
        b (int): The second number.

    Returns:
        TaskId: The task ID.
    """
    task = tasks.add.delay(a, b)
    return TaskId(task_id=task.id)


# This route is protected by the get_current_username dependency
# This means that the client must send a valid token in the Authorization
# header to access this route, and the username of the token will be
# available in the get_current_username function, but it won't be used
# in this route.
@router.get("/get-result")
async def get_task_result(task_id: str):
    """Get the result of a task.

    This function returns the result of a task given its ID.

    Args:
        task_id (str): The ID of the task.

    Returns:
        dict: The status of the task and its result.
    """
    task = tasks.add.AsyncResult(task_id)
    if not task.ready():
        return {"status": "PENDING"}
    return {"status": "SUCCESS", "result": task.get()}


@router.get("/get-sellers")
async def get_sellers() -> schemas.GetSellersResponse:
    """Get sellers in tienda"""
    task = tasks.get_sellers.delay()
    return task.get()


@router.get("/get-seller/{seller_id}")
async def get_seller(seller_id: int) -> schemas.SellerBase:
    """Get seller by ID"""
    task = tasks.get_seller.delay(seller_id)
    return task.get()


@router.post("/add-seller")
async def add_seller(name: str) -> schemas.AddSellerResponse:
    """Add a new seller"""
    task = tasks.add_seller.delay(name)
    return task.get()


@router.put("/update-seller/{seller_id}")
async def update_seller(seller_id: int, name: str):
    """Update a seller"""
    task = tasks.update_seller.delay(seller_id, name)
    return task.get()


@router.delete("/delete-seller/{seller_id}")
async def delete_seller(seller_id: int):
    """Delete a seller"""
    task = tasks.delete_seller.delay(seller_id)
    return task.get()
