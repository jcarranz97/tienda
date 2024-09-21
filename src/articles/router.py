#!/usr/bin/env python
"""Router for the API for article management."""
from fastapi import APIRouter
from . import schemas
from . import tasks

router = APIRouter()


@router.get("/get-articles-statuses")
async def get_articles_statuses() -> schemas.GetArticlesStatusesResponse:
    """Get all articles statuses"""
    task = tasks.get_article_statuses.delay()
    return task.get()


@router.get("/get-article-status/{id_article_status}")
async def get_article_status(id_article_status: int) -> schemas.ArticleStatusBase:
    """Get an article status"""
    task = tasks.get_article_status.delay(id_article_status)
    return task.get()


@router.get("/add-article-status")
async def add_article_status(name: str) -> int:
    """Add an article status"""
    task = tasks.add_article_status.delay(name)
    return task.get()


@router.put("/modify-article-status/{id_article_status}")
async def modify_article_status(id_article_status: int, name: str) -> int:
    """Modify an article status"""
    task = tasks.modify_article_status.delay(id_article_status, name)
    return task.get()


@router.delete("/delete-article-status/{id_article_status}")
async def delete_article_status(id_article_status: int) -> int:
    """Delete an article status"""
    task = tasks.delete_article_status.delay(id_article_status)
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
async def get_articles(
        shipping_group_name: str | None = None,
        ) -> schemas.GetArticlesDetailResponse:
    """Get all articles"""
    task = tasks.get_articles.delay(
        shipping_group_name=shipping_group_name,
    )
    return task.get()


@router.get("/get-article/{article_id}")
async def get_article(article_id: int) -> schemas.ArticleDetailResponse:
    """Get an article"""
    task = tasks.get_article.delay(article_id)
    return task.get()


@router.get("/get-article-by-shipping-group-and-label")
async def get_article_by_shipping_group_and_label(
    shipping_group_name: str,
    shipping_label: str,
) -> schemas.ArticleDetailResponse:
    """Get an article by shipping group and label"""
    task = tasks.get_article_by_shipping_group_and_label.delay(
        shipping_group_name=shipping_group_name,
        shipping_label=shipping_label,
    )
    return task.get()


@router.get("/add-article")
async def add_article(
    description: str,
    shipping_label: str,
    purchase_price: float,
    article_location: str,
    article_status: str,
    shipping_group_name: str | None = None,
) -> int:
    """Add an article"""
    task = tasks.add_article.delay(
        description,
        shipping_label,
        purchase_price,
        article_location=article_location,
        article_status=article_status,
        shipping_group_name=shipping_group_name,
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


@router.post("/add-sale-price")
async def add_sale_price(
        shipping_group_name: str,
        shipping_label: str,
        sale_price: float,
) -> int:
    """Add a sale price"""
    task = tasks.add_sale_price.delay(
        shipping_group_name=shipping_group_name,
        shipping_label=shipping_label,
        sale_price=sale_price,
    )
    return task.get()
