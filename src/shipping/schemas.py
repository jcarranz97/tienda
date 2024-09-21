#!/usr/bin/python3
"""Seller schemas"""
from datetime import datetime
from pydantic import BaseModel


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
