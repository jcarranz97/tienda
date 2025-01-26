#!/usr/bin/env python
"""Router for the API for shipping """
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


@router.get("/get-shipping-statuses")
async def get_shipping_statuses(
    current_user: Annotated[User, Depends(get_current_user)],
) -> schemas.GetShippingStatusesResponse:
    """Get all shipping statuses"""
    task = tasks.get_shipping_statuses.delay()
    return task.get()


@router.get("/get-shipping-status/{status_id}")
async def get_shipping_status(
    status_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
) -> schemas.ShippingStatusBase:
    """Get a shipping status"""
    task = tasks.get_shipping_status.delay(status_id)
    return task.get()


@router.post("/add-shipping-status")
async def add_shipping_status(
    name: str,
    description: str,
    current_user: Annotated[User, Depends(get_current_user)],
) -> int:
    """Add a shipping status"""
    task = tasks.add_shipping_status.delay(name, description)
    return task.get()


@router.put("/update-shipping-status/{status_id}")
async def update_shipping_status(
        status_id: int,
        name: str,
        description: str,
        current_user: Annotated[User, Depends(get_current_user)],
) -> int:
    """Update a shipping status"""
    task = tasks.update_shipping_status.delay(status_id, name, description)
    return task.get()


@router.delete("/delete-shipping-status/{status_id}")
async def delete_shipping_status(
    status_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
) -> int:
    """Delete a shipping status"""
    task = tasks.delete_shipping_status.delay(status_id)
    return task.get()


@router.get("/get-shipping-groups")
async def get_shipping_groups(
    current_user: Annotated[User, Depends(get_current_user)],
) -> schemas.GetShippingGroupsResponse:
    """Get all shipping groups"""
    task = tasks.get_shipping_groups.delay()
    return task.get()


@router.get("/get-shipping-group/{group_id}")
async def get_shipping_group(
    group_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
) -> schemas.ShippingGroupBase:
    """Get a shipping group"""
    task = tasks.get_shipping_group.delay(group_id)
    return task.get()


@router.post("/add-shipping-group")
async def add_shipping_group(
    shipping_group: schemas.AddShippingGroupInput,
    current_user: Annotated[User, Depends(get_current_user)],
) -> int:
    """Add a shipping group"""
    task = tasks.add_shipping_group.delay(
        name=shipping_group.name,
        id_shipper=shipping_group.id_shipper,
        id_status=shipping_group.id_status,
        shipping_cost=shipping_group.shipping_cost,
        dollar_price=shipping_group.dollar_price,
        tax=shipping_group.tax,
        notes=shipping_group.notes,
    )
    return task.get()


@router.put("/update-shipping-group/{group_id}")
async def update_shipping_group(
        id_shipping_group: int,
        current_user: Annotated[User, Depends(get_current_user)],
        name: str | None = None,
        id_shipper: int | None = None,
        id_status: int | None = None,
        shipping_cost: float | None = None,
        dollar_price: float | None = None,
        tax: float | None = None,
        notes: str | None = None,
        ) -> schemas.UpdateShippingGroupResponse:
    """Update a shipping group"""
    task = tasks.update_shipping_group.delay(
        id_shipping_group=id_shipping_group,
        name=name,
        id_shipper=id_shipper,
        id_status=id_status,
        shipping_cost=shipping_cost,
        dollar_price=dollar_price,
        tax=tax,
        notes=notes,
    )
    return task.get()


@router.delete("/delete-shipping-group/{group_id}")
async def delete_shipping_group(
    group_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
) -> int:
    """Delete a shipping group"""
    task = tasks.delete_shipping_group.delay(group_id)
    return task.get()
