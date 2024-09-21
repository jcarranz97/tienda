#!/usr/bin/env python
"""Celery tasks related to group2."""
from celery import shared_task
from sqlalchemy import select
from sqlalchemy import func
from sqlalchemy.orm import aliased
from database import Session
from shipping.models import ShippingGroup
from . import models
from . import schemas


@shared_task
def get_articles_availabilities():
    """Get articles availabilities from database"""
    with Session() as session:
        db_availabilities = session.scalars(
            select(models.ArticleAvailability)
        ).all()
        availabilities = [
            schemas.ArticleAvailabilityBase(
                id=db_availability.id_availability,
                name=db_availability.availability_name,
                created_at=db_availability.created_at,
                updated_at=db_availability.updated_at,
            ).dict()
            for db_availability in db_availabilities
        ]
        return schemas.GetArticlesAvailabilitiesResponse(
            availabilities=availabilities
        ).dict()


@shared_task
def get_article_availability(availability_id: int):
    """Get article availability from database"""
    with Session() as session:
        db_availability = session.scalar(
            select(models.ArticleAvailability)
            .where(
                models.ArticleAvailability.id_availability == availability_id
            )
        )
        if not db_availability:
            raise ValueError(
                f"Article availability with ID {availability_id} not found.")
        return schemas.ArticleAvailabilityBase(
            id=db_availability.id_availability,
            name=db_availability.availability_name,
            created_at=db_availability.created_at,
            updated_at=db_availability.updated_at,
        ).dict()


@shared_task
def add_article_availability(name: str):
    """Add article availability to database"""
    with Session() as session:
        # Before adding a new article availability, we should confirm that
        # there is not article availability with the same name in the database.
        # This is a business rule that should be enforced.
        db_availability = session.scalar(
            select(models.ArticleAvailability)
            .where(models.ArticleAvailability.availability_name == name)
        )
        if db_availability:
            raise ValueError(
                f"Article availability '{name}' already exists in" +
                "the database.")

        new_availability = models.ArticleAvailability(availability_name=name)
        session.add(new_availability)
        session.commit()
        return new_availability.id_availability


@shared_task
def modify_article_availability(availability_id: int, name: str):
    """Modify article availability by availability_id"""
    with Session() as session:
        db_availability = session.scalar(
            select(models.ArticleAvailability)
            .where(
                models.ArticleAvailability.id_availability == availability_id
            )
        )
        if not db_availability:
            raise ValueError(
                f"Article availability with ID {availability_id} not found.")
        db_availability.availability_name = name
        session.commit()
        return availability_id


@shared_task
def delete_article_availability(availability_id: int):
    """Delete article availability by availability_id"""
    with Session() as session:
        db_availability = session.scalar(
            select(models.ArticleAvailability)
            .where(
                models.ArticleAvailability.id_availability == availability_id
            )
        )
        if not db_availability:
            raise ValueError(
                f"Article availability with ID {availability_id} not found.")
        session.delete(db_availability)
        session.commit()
        return availability_id


@shared_task
def get_locations():
    """Get locations from database"""
    with Session() as session:
        db_locations = session.scalars(select(models.Location)).all()
        locations = [
            schemas.LocationBase(
                id=db_location.id_location,
                name=db_location.location_name,
                created_at=db_location.created_at,
                updated_at=db_location.updated_at,
            ).dict()
            for db_location in db_locations
        ]
        return schemas.GetLocationsResponse(locations=locations).dict()


@shared_task
def get_location(location_id: int):
    """Get location from database"""
    with Session() as session:
        db_location = session.scalar(
            select(models.Location)
            .where(models.Location.id_location == location_id)
        )
        if not db_location:
            raise ValueError(f"Location with ID {location_id} not found.")
        return schemas.LocationBase(
            id=db_location.id_location,
            name=db_location.location_name,
            created_at=db_location.created_at,
            updated_at=db_location.updated_at,
        ).dict()


@shared_task
def add_location(name: str):
    """Add location to database"""
    with Session() as session:
        # Before adding a new location, we should confirm that there is no
        # location with the same name in the database. This is a business rule
        # that should be enforced.
        db_location = session.scalar(
            select(models.Location)
            .where(models.Location.location_name == name)
        )
        if db_location:
            raise ValueError(
                f"Location '{name}' already exists in the database.")

        new_location = models.Location(location_name=name)
        session.add(new_location)
        session.commit()
        return new_location.id_location


@shared_task
def modify_location(location_id: int, name: str):
    """Modify location by location_id"""
    with Session() as session:
        db_location = session.scalar(
            select(models.Location)
            .where(models.Location.id_location == location_id)
        )
        if not db_location:
            raise ValueError(f"Location with ID {location_id} not found.")
        db_location.location_name = name
        session.commit()
        return location_id


@shared_task
def delete_location(location_id: int):
    """Delete location by location_id"""
    with Session() as session:
        db_location = session.scalar(
            select(models.Location)
            .where(models.Location.id_location == location_id)
        )
        if not db_location:
            raise ValueError(f"Location with ID {location_id} not found.")
        session.delete(db_location)
        session.commit()
        return location_id


# @shared_task
# def get_articles():
#     """Get articles from database"""
#     with Session() as session:
#         db_articles = session.scalars(select(models.Article)).all()
#         articles = [
#             schemas.ArticleBase(
#                 id=db_article.id_article,
#                 description=db_article.description,
#                 shipping_label=db_article.shipping_label,
#                 purchase_price=db_article.purchase_price,
#                 sale_price=db_article.sale_price,
#                 id_availability=db_article.id_availability,
#                 id_location=db_article.id_location,
#                 id_shipping_group=db_article.id_shipping_group,
#                 created_at=db_article.created_at,
#                 updated_at=db_article.updated_at,
#             ).dict()
#             for db_article in db_articles
#         ]
#         return schemas.GetArticlesResponse(articles=articles).dict()
@shared_task
def get_articles():
    """Get articles from database"""
    with Session() as session:
        # Create an alias for the subquery counting articles per shipping group
        article_count_subquery = (
            select(
                models.Article.id_shipping_group,
                func.count(models.Article.id_article).label('article_count')
            )
            .group_by(models.Article.id_shipping_group)
            .subquery()
        )

        # Create an alias to work with the subquery
        ArticleCount = aliased(article_count_subquery)

        # Main query using ORM models
        query = (
            session.query(
                models.Article.id_article,
                models.Article.description,
                models.Article.shipping_label,
                models.Article.purchase_price,
                ShippingGroup.shipping_group_name,
                ShippingGroup.dollar_price,
                ShippingGroup.tax,
                ShippingGroup.shipping_cost,
                models.Location.location_name,
                models.Article.sale_price,
                (models.Article.purchase_price * ShippingGroup.dollar_price * (1 + (ShippingGroup.tax * 0.01)) +
                 (ShippingGroup.shipping_cost / ArticleCount.c.article_count)).label('purchase_price_mx')
            )
            .join(ShippingGroup, models.Article.id_shipping_group == ShippingGroup.id_shipping_group)
            .join(models.Location, models.Article.id_location == models.Location.id_location)
            .join(ArticleCount, models.Article.id_shipping_group == ArticleCount.c.id_shipping_group)
        )

        articles = [
            schemas.ArticleDetailResponse(
                id_article=db_article.id_article,
                description=db_article.description,
                shipping_label=db_article.shipping_label,
                purchase_price=db_article.purchase_price,
                shipping_group_name=db_article.shipping_group_name,
                dollar_price=db_article.dollar_price,
                tax=db_article.tax,
                shipping_cost=db_article.shipping_cost,
                location_name=db_article.location_name,
                purchase_price_mxn=db_article.purchase_price_mx,
                sale_price=db_article.sale_price,
            ).dict()
            for db_article in query.all()
        ]
        return schemas.GetArticlesDetailResponse(articles=articles).dict()


@shared_task
def get_article(article_id: int):
    """Get article from database"""
    with Session() as session:
        db_article = session.scalar(
            select(models.Article)
            .where(models.Article.id_article == article_id)
        )
        if not db_article:
            raise ValueError(f"Article with ID {article_id} not found.")
        return schemas.ArticleBase(
            id=db_article.id_article,
            description=db_article.description,
            shipping_label=db_article.shipping_label,
            purchase_price=db_article.purchase_price,
            sale_price=db_article.sale_price,
            id_availability=db_article.id_availability,
            id_location=db_article.id_location,
            id_shipping_group=db_article.id_shipping_group,
            created_at=db_article.created_at,
            updated_at=db_article.updated_at,
        ).dict()


@shared_task
def add_article(
    description: str,
    shipping_label: str,
    purchase_price: float,
    availability_id: int,
    location_id: int,
    shipping_group_id: int = None,
):
    """Add article to database"""
    with Session() as session:
        new_article = models.Article(
            description=description,
            shipping_label=shipping_label,
            purchase_price=purchase_price,
            id_availability=availability_id,
            id_location=location_id,
            id_shipping_group=shipping_group_id,
        )
        session.add(new_article)
        session.commit()
        return new_article.id_article


@shared_task
def modify_article(
    article_id: int,
    description: str | None = None,
    shipping_label: str | None = None,
    purchase_price: float | None = None,
    sale_price: float | None = None,
    availability_id: int | None = None,
    location_id: int | None = None,
    shipping_group_id: int | None = None,
):
    """Modify article by article_id"""
    with Session() as session:
        db_article = session.scalar(
            select(models.Article)
            .where(models.Article.id_article == article_id)
        )
        if not db_article:
            raise ValueError(f"Article with ID {article_id} not found.")
        # Only update the fields that are not None in the request.
        # If all fields are None, the article will not be modified. This is
        # should trigger a validation error in the API.
        item_modifications = 0
        if description is not None:
            db_article.description = description
            item_modifications += 1
        if shipping_label is not None:
            db_article.shipping_label = shipping_label
            item_modifications += 1
        if purchase_price is not None:
            db_article.purchase_price = purchase_price
            item_modifications += 1
        if sale_price is not None:
            db_article.sale_price = sale_price
            item_modifications += 1
        if availability_id is not None:
            db_article.id_availability = availability_id
            item_modifications += 1
        if location_id is not None:
            db_article.id_location = location_id
            item_modifications += 1
        if shipping_group_id is not None:
            db_article.id_shipping_group = shipping_group_id
            item_modifications += 1
        if item_modifications == 0:
            raise ValueError("No fields to modify.")
        session.commit()
        return schemas.ModifyArticleResponse(
            id=article_id, modified_items=item_modifications
        ).dict()


@shared_task
def delete_article(article_id: int):
    """Delete article by article_id"""
    with Session() as session:
        db_article = session.scalar(
            select(models.Article)
            .where(models.Article.id_article == article_id)
        )
        if not db_article:
            raise ValueError(f"Article with ID {article_id} not found.")
        session.delete(db_article)
        session.commit()
        return article_id
