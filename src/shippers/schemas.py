#!/usr/bin/python3
"""Seller schemas"""
from datetime import datetime
from pydantic import BaseModel


class ShipperBase(BaseModel):
    """Shipper base schema"""
    id: int
    name: str
    created_at: datetime
    updated_at: datetime


class GetShippersResponse(BaseModel):
    """Get shippers response schema"""
    shippers: list[ShipperBase]
