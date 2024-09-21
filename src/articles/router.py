#!/usr/bin/env python
"""Router for the API for article management."""
from fastapi import APIRouter
from . import schemas
from . import tasks

router = APIRouter()


@router.get("/get-articles-availabilities")
async def get_articles_availabilities() -> schemas.GetArticlesAvailabilitiesResponse:
    """Get all articles availabilities"""
    task = tasks.get_articles_availabilities.delay()
    return task.get()


@router.get("/get-article-availability/{availability_id}")
async def get_article_availability(availability_id: int) -> schemas.ArticleAvailabilityBase:
    """Get an article availability"""
    task = tasks.get_article_availability.delay(availability_id)
    return task.get()


@router.get("/add-article-availability")
async def add_article_availability(name: str) -> int:
    """Add an article availability"""
    task = tasks.add_article_availability.delay(name)
    return task.get()


@router.put("/modify-article-availability/{availability_id}")
async def modify_article_availability(availability_id: int, name: str) -> int:
    """Modify an article availability"""
    task = tasks.modify_article_availability.delay(availability_id, name)
    return task.get()


@router.delete("/delete-article-availability/{availability_id}")
async def delete_article_availability(availability_id: int) -> int:
    """Delete an article availability"""
    task = tasks.delete_article_availability.delay(availability_id)
    return task.get()


# Location routes
@router.get("/get-locations")
async def get_locations() -> schemas.GetLocationsResponse:
    """Get all locations"""
    task = tasks.get_locations.delay()
    return task.get()


@router.get("/get-location/{location_id}")
async def get_location(location_id: int) -> schemas.LocationBase:
    """Get a location"""
    task = tasks.get_location.delay(location_id)
    return task.get()


@router.get("/add-location")
async def add_location(name: str) -> int:
    """Add a location"""
    task = tasks.add_location.delay(name)
    return task.get()


@router.put("/modify-location/{location_id}")
async def modify_location(location_id: int, name: str) -> int:
    """Modify a location"""
    task = tasks.modify_location.delay(location_id, name)
    return task.get()


@router.delete("/delete-location/{location_id}")
async def delete_location(location_id: int) -> int:
    """Delete a location"""
    task = tasks.delete_location.delay(location_id)
    return task.get()


# Article routes
@router.get("/get-articles")
async def get_articles() -> schemas.GetArticlesDetailResponse:
    """Get all articles"""
    task = tasks.get_articles.delay()
    return task.get()


@router.get("/get-article/{article_id}")
async def get_article(article_id: int) -> schemas.ArticleDetailResponse:
    """Get an article"""
    task = tasks.get_article.delay(article_id)
    return task.get()


@router.get("/add-article")
async def add_article(
    description: str,
    shipping_label: str,
    purchase_price: float,
    id_availability: int,
    id_location: int,
    id_shipping_group: int | None = None,
) -> int:
    """Add an article"""
    task = tasks.add_article.delay(
        description,
        shipping_label,
        purchase_price,
        id_availability,
        id_location,
        id_shipping_group,
    )
    return task.get()


@router.put("/modify-article/{article_id}")
async def modify_article(
    article_id: int,
    description: str | None = None,
    shipping_label: str | None = None,
    purchase_price: float | None = None,
    id_availability: int | None = None,
    id_location: int | None = None,
    id_shipping_group: int | None = None,
    sale_price: float | None = None,
) -> schemas.ModifyArticleResponse:
    """Modify an article"""
    task = tasks.modify_article.delay(
        article_id=article_id,
        description=description,
        shipping_label=shipping_label,
        purchase_price=purchase_price,
        sale_price=sale_price,
        id_availability=id_availability,
        id_location=id_location,
        id_shipping_group=id_shipping_group,
    )
    return task.get()


@router.delete("/delete-article/{article_id}")
async def delete_article(article_id: int) -> int:
    """Delete an article"""
    task = tasks.delete_article.delay(article_id)
    return task.get()
