#!/usr/bin/env python
"""Router for the API for shipping """
from fastapi import APIRouter
from . import schemas
from . import tasks

router = APIRouter()


@router.get("/get-shipping-statuses")
async def get_shipping_statuses() -> schemas.GetShippingStatusesResponse:
    """Get all shipping statuses"""
    task = tasks.get_shipping_statuses.delay()
    return task.get()


@router.get("/get-shipping-status/{status_id}")
async def get_shipping_status(status_id: int) -> schemas.ShippingStatusBase:
    """Get a shipping status"""
    task = tasks.get_shipping_status.delay(status_id)
    return task.get()


@router.post("/add-shipping-status")
async def add_shipping_status(name: str, description: str) -> int:
    """Add a shipping status"""
    task = tasks.add_shipping_status.delay(name, description)
    return task.get()


@router.put("/modify-shipping-status/{status_id}")
async def modify_shipping_status(
        status_id: int,
        name: str,
        description: str,
) -> int:
    """Modify a shipping status"""
    task = tasks.modify_shipping_status.delay(status_id, name, description)
    return task.get()


@router.delete("/delete-shipping-status/{status_id}")
async def delete_shipping_status(status_id: int) -> int:
    """Delete a shipping status"""
    task = tasks.delete_shipping_status.delay(status_id)
    return task.get()
