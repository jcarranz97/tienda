#!/usr/bin/python3
"""Seller schemas"""
from datetime import datetime
from pydantic import BaseModel


class SellerBase(BaseModel):
    """Seller base schema"""
    id: int
    name: str
    created_at: datetime
    updated_at: datetime


class GetSellersResponse(BaseModel):
    """Get sellers response schema"""
    sellers: list[SellerBase]


class AddSellerResponse(BaseModel):
    """Add seller response schema"""
    id: int
