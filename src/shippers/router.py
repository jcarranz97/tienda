#!/usr/bin/env python
"""Router for the API for shippers"""
from fastapi import APIRouter
from . import schemas
from . import tasks

router = APIRouter()


@router.get("/get-shippers")
async def get_shippers() -> schemas.GetShippersResponse:
    """Get all shippers"""
    task = tasks.get_shippers.delay()
    return task.get()


@router.get("/get-shippers/{shipper_id}")
async def get_shipper(shipper_id: int) -> schemas.ShipperBase:
    """Get a shipper"""
    task = tasks.get_shipper.delay(shipper_id)
    return task.get()


@router.post("/add-shipper")
async def add_shipper(name: str) -> int:
    """Add a shipper"""
    task = tasks.add_shipper.delay(name)
    return task.get()


@router.put("/modify-shipper/{shipper_id}")
async def modify_shipper(shipper_id: int, name: str) -> int:
    """Modify a shipper"""
    task = tasks.modify_shipper.delay(shipper_id, name)
    return task.get()


@router.delete("/delete-shipper/{shipper_id}")
async def delete_shipper(shipper_id: int) -> int:
    """Delete a shipper"""
    task = tasks.delete_shipper.delay(shipper_id)
    return task.get()
