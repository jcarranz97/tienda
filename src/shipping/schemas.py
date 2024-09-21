#!/usr/bin/python3
"""Seller schemas"""
from datetime import datetime
from pydantic import BaseModel
from shippers.schemas import ShipperBase


class ShippingStatusBase(BaseModel):
    """Shipper base schema"""
    id: int
    name: str
    description: str
    created_at: datetime
    updated_at: datetime


class GetShippingStatusesResponse(BaseModel):
    """Get shipping statuses response schema"""
    statuses: list[ShippingStatusBase]


class ShippingGroupBase(BaseModel):
    """Shipping group base schema"""
    id: int
    name: str
    id_shipper: int
    id_status: int
    shipping_cost: float
    dollar_price: float
    tax: float
    created_at: datetime
    updated_at: datetime
    notes: str | None


class GetShippingGroupsResponse(BaseModel):
    """Get shipping groups response schema"""
    groups: list[ShippingGroupBase]


class UpdateShippingGroupResponse(BaseModel):
    """Update shipping group response schema"""
    id: int
    num_changes: int
