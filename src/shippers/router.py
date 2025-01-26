#!/usr/bin/env python
"""Router for the API for shippers"""
from fastapi import APIRouter
from fastapi import Depends
from typing import Annotated
from . import schemas
from . import tasks
from auth.auth import (
    get_current_user,
)
from auth.models import (
    User,
)

router = APIRouter()


@router.get("/get-shippers")
async def get_shippers(
    current_user: Annotated[User, Depends(get_current_user)],
) -> schemas.GetShippersResponse:
    """Get all shippers"""
    task = tasks.get_shippers.delay()
    return task.get()


@router.get("/get-shippers/{shipper_id}")
async def get_shipper(
    shipper_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
) -> schemas.ShipperBase:
    """Get a shipper"""
    task = tasks.get_shipper.delay(shipper_id)
    return task.get()


@router.post("/add-shipper")
async def add_shipper(
    name: str,
    current_user: Annotated[User, Depends(get_current_user)],
) -> int:
    """Add a shipper"""
    task = tasks.add_shipper.delay(name)
    return task.get()


@router.put("/update-shipper/{shipper_id}")
async def update_shipper(
    shipper_id: int,
    name: str,
    current_user: Annotated[User, Depends(get_current_user)],
) -> int:
    """Update a shipper"""
    task = tasks.update_shipper.delay(shipper_id, name)
    return task.get()


@router.delete("/delete-shipper/{shipper_id}")
async def delete_shipper(
    shipper_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
) -> int:
    """Delete a shipper"""
    task = tasks.delete_shipper.delay(shipper_id)
    return task.get()
