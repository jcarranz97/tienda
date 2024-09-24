#!/usr/bin/python3
"""Seller schemas"""
from datetime import datetime
from pydantic import BaseModel


class ProductStatusBase(BaseModel):
    """product availability base schema"""
    id: int
    name: str
    created_at: datetime
    updated_at: datetime


class GetproductsStatusesResponse(BaseModel):
    """Get products statuses response schema"""
    statuses: list[ProductStatusBase]


class LocationBase(BaseModel):
    """Location base schema"""
    id: int
    name: str
    created_at: datetime
    updated_at: datetime


class GetLocationsResponse(BaseModel):
    """Get locations response schema"""
    locations: list[LocationBase]


class productBase(BaseModel):
    """product base schema"""
    id: int
    description: str
    shipping_label: str
    purchase_price: float | None
    sale_price: float | None
    id_product_status: int
    id_location: int
    id_shipping_group: int | None
    created_at: datetime
    updated_at: datetime


class productDetailResponse(BaseModel):
    """product detail response schema"""
    id_product: int
    description: str
    shipping_label: str
    purchase_price: float | None
    shipping_group: str | None
    status: str
    location_name: str
    purchase_price_mxn: float | None
    sale_price: float | None
    profit: float | None


class GetproductsResponse(BaseModel):
    """Get products response schema"""
    products: list[productBase]


class GetproductsDetailResponse(BaseModel):
    """Get products detail response schema"""
    products: list[productDetailResponse]
    num_products: int


class UpdateproductResponse(BaseModel):
    """Update product response schema"""
    id: int
    updated_items: int
