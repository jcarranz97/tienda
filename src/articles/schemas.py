#!/usr/bin/python3
"""Seller schemas"""
from datetime import datetime
from pydantic import BaseModel


class ArticleAvailabilityBase(BaseModel):
    """Article availability base schema"""
    id: int
    name: str
    created_at: datetime
    updated_at: datetime


class GetArticlesAvailabilitiesResponse(BaseModel):
    """Get articles availabilities response schema"""
    availabilities: list[ArticleAvailabilityBase]


class LocationBase(BaseModel):
    """Location base schema"""
    id: int
    name: str
    created_at: datetime
    updated_at: datetime


class GetLocationsResponse(BaseModel):
    """Get locations response schema"""
    locations: list[LocationBase]


class ArticleBase(BaseModel):
    """Article base schema"""
    id: int
    description: str
    shipping_label: str
    purchase_price: float
    id_availability: int
    id_location: int
    id_shipping_group: int
    created_at: datetime
    updated_at: datetime


class GetArticlesResponse(BaseModel):
    """Get articles response schema"""
    articles: list[ArticleBase]


class ModifyArticleResponse(BaseModel):
    """Modify article response schema"""
    id: int
    modified_items: int
