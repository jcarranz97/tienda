#!/usr/bin/python3
"""Seller schemas"""
from datetime import datetime
from pydantic import BaseModel


class ArticleStatusBase(BaseModel):
    """Article availability base schema"""
    id: int
    name: str
    created_at: datetime
    updated_at: datetime


class GetArticlesStatusesResponse(BaseModel):
    """Get articles statuses response schema"""
    statuses: list[ArticleStatusBase]


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
    purchase_price: float | None
    sale_price: float | None
    id_article_status: int
    id_location: int
    id_shipping_group: int | None
    created_at: datetime
    updated_at: datetime


class ArticleDetailResponse(BaseModel):
    """Article detail response schema"""
    id_article: int
    description: str
    shipping_label: str
    purchase_price: float | None
    shipping_group_name: str | None
    dollar_price: float | None
    tax: float | None
    shipping_cost: float | None
    location_name: str
    purchase_price_mxn: float | None
    sale_price: float | None
    profit: float | None


class GetArticlesResponse(BaseModel):
    """Get articles response schema"""
    articles: list[ArticleBase]


class GetArticlesDetailResponse(BaseModel):
    """Get articles detail response schema"""
    articles: list[ArticleDetailResponse]


class ModifyArticleResponse(BaseModel):
    """Modify article response schema"""
    id: int
    modified_items: int
