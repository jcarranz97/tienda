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


@router.get("/get-shipping-groups")
async def get_shipping_groups() -> schemas.GetShippingGroupsResponse:
    """Get all shipping groups"""
    task = tasks.get_shipping_groups.delay()
    return task.get()


@router.get("/get-shipping-group/{group_id}")
async def get_shipping_group(group_id: int) -> schemas.ShippingGroupBase:
    """Get a shipping group"""
    task = tasks.get_shipping_group.delay(group_id)
    return task.get()


# pylint: disable=too-many-arguments
@router.post("/add-shipping-group")
async def add_shipping_group(
        name: str,
        id_shipper: int,
        id_status: int,
        shipping_cost: float,
        dollar_price: float,
        tax: float,
        notes: str | None,
) -> int:
    """Add a shipping group"""
    task = tasks.add_shipping_group.delay(
        name, id_shipper, id_status, shipping_cost, dollar_price, tax, notes
    )
    return task.get()
