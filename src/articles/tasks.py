#!/usr/bin/env python
"""Celery tasks related to group2."""
from celery import shared_task
from sqlalchemy import select
from database import Session
from shipping.queries import get_shipping_group_by_name
from . import models
from . import schemas
from . import queries


@shared_task
def get_article_statuses():
    """Get article statuses from database"""
    with Session() as session:
        db_statuses = session.scalars(select(models.ArticleStatus)).all()
        statuses = [
            schemas.ArticleStatusBase(
                id=db_status.id_article_status,
                name=db_status.status_name,
                created_at=db_status.created_at,
                updated_at=db_status.updated_at,
            ).dict()
            for db_status in db_statuses
        ]
        return schemas.GetArticlesStatusesResponse(statuses=statuses).dict()


@shared_task
def get_article_status(id_article_status: int):
    """Get article status from database"""
    with Session() as session:
        db_status = session.scalar(
            select(models.ArticleStatus)
            .where(
                models.ArticleStatus.id_article_status == id_article_status
            )
        )
        if not db_status:
            raise ValueError(
                f"Article status with ID {id_article_status} not found.")
        return schemas.ArticleStatusBase(
            id=db_status.id_article_status,
            name=db_status.status_name,
            created_at=db_status.created_at,
            updated_at=db_status.updated_at,
        ).dict()


@shared_task
def add_article_status(name: str):
    """Add article status to database"""
    with Session() as session:
        # Before adding a new status, we should confirm that there is no status
        # with the same name in the database. This is a business rule that
        # should be enforced.
        db_status = session.scalar(
            select(models.ArticleStatus)
            .where(models.ArticleStatus.status_name == name)
        )
        if db_status:
            raise ValueError(
                f"Article status '{name}' already exists in the database.")

        new_status = models.ArticleStatus(status_name=name)
        session.add(new_status)
        session.commit()
        return new_status.id_article_status


@shared_task
def modify_article_status(id_article_status: int, name: str):
    """Modify article status by id_article_status"""
    with Session() as session:
        db_status = session.scalar(
            select(models.ArticleStatus)
            .where(models.ArticleStatus.id_article_status == id_article_status)
        )
        if not db_status:
            raise ValueError(
                f"Article status with ID {id_article_status} not found.")
        db_status.status_name = name
        session.commit()
        return id_article_status


@shared_task
def delete_article_status(id_article_status: int):
    """Delete article status by id_article_status"""
    with Session() as session:
        db_status = session.scalar(
            select(models.ArticleStatus)
            .where(models.ArticleStatus.id_article_status == id_article_status)
        )
        if not db_status:
            raise ValueError(
                f"Article status with ID {id_article_status} not found.")
        session.delete(db_status)
        session.commit()
        return id_article_status


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


@shared_task
def get_articles(shipping_group_name: str | None = None):
    """Get articles from database"""
    with Session() as session:
        # Before fetching the articles, we need to confirm that
        # shipping_group_name is valid (If entered),
        if shipping_group_name:
            db_shipping_group = get_shipping_group_by_name(
                session=session,
                shipping_group_name=shipping_group_name,
            )
        # Main query to fetch the required fields, including the "profit"
        query = queries.get_article_query(
            session=session,
            id_shipping_group=db_shipping_group.id_shipping_group if shipping_group_name else None,  # noqa: E501, pylint: disable=line-too
        )

        articles = [
            schemas.ArticleDetailResponse(
                id_article=db_article.id_article,
                description=db_article.description,
                shipping_label=db_article.shipping_label,
                purchase_price=db_article.purchase_price,
                shipping_group=db_article.shipping_group_name,
                status=db_article.status_name,
                dollar_price=db_article.dollar_price,
                tax=db_article.tax,
                shipping_cost=db_article.shipping_cost,
                location_name=db_article.location_name,
                purchase_price_mxn=db_article.purchase_price_mxn,
                sale_price=db_article.sale_price,
                profit=db_article.profit,
            ).dict()
            for db_article in query.all()
        ]
        return schemas.GetArticlesDetailResponse(articles=articles).dict()


@shared_task
def get_article(article_id: int):
    """Get article from database"""
    # Same as get_articles, but with a filter by article_id in the query
    with Session() as session:
        query = queries.get_article_query(session, article_id)

        db_article = query.first()
        if not db_article:
            raise ValueError(f"Article with ID {article_id} not found.")
        return schemas.ArticleDetailResponse(
            id_article=db_article.id_article,
            description=db_article.description,
            shipping_label=db_article.shipping_label,
            purchase_price=db_article.purchase_price,
            shipping_group=db_article.shipping_group_name,
            status=db_article.status_name,
            dollar_price=db_article.dollar_price,
            tax=db_article.tax,
            shipping_cost=db_article.shipping_cost,
            location_name=db_article.location_name,
            purchase_price_mxn=db_article.purchase_price_mxn,
            profit=db_article.profit,
            sale_price=db_article.sale_price,
        ).dict()


@shared_task
def add_article(
    description: str,
    shipping_label: str,
    purchase_price: float,
    id_article_status: int,
    location_id: int,
    shipping_group_name: str | None = None,
):
    """Add article to database"""
    with Session() as session:
        if shipping_group_name:
            db_shipping_group = get_shipping_group_by_name(
                session=session,
                shipping_group_name=shipping_group_name,
            )
        new_article = models.Article(
            description=description,
            shipping_label=shipping_label,
            purchase_price=purchase_price,
            id_article_status=id_article_status,
            id_location=location_id,
            id_shipping_group=db_shipping_group.id_shipping_group if shipping_group_name else None,  # noqa: E501, pylint: disable=line-too-long
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
    id_article_status: int | None = None,
    id_location: int | None = None,
    id_shipping_group: int | None = None,
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
        if id_article_status is not None:
            db_article.id_article_status = id_article_status
            item_modifications += 1
        if id_location is not None:
            db_article.id_location = id_location
            item_modifications += 1
        if id_shipping_group is not None:
            db_article.id_shipping_group = id_shipping_group
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


@shared_task
def add_sale_price(
        shipping_group_name: str,
        shipping_label: str,
        sale_price: float,
) -> int:
    """Add sale price to database"""
    with Session() as session:
        # Before adding a new sale price, we should confirm that the
        # shipping_group_name is valid.
        db_shipping_group = get_shipping_group_by_name(
            session=session,
            shipping_group_name=shipping_group_name,
        )

        db_article = session.scalar(
            select(models.Article)
            .where(
                models.Article.shipping_label == shipping_label,
                models.Article.id_shipping_group == db_shipping_group.id_shipping_group  # noqa: E501, pylint: disable=line-too-long
            )
        )
        if not db_article:
            raise ValueError(
                f"Article with shipping label '{shipping_label}' not found " +
                "in the shipping group '{shipping_group_name}'.")
        db_article.sale_price = sale_price
        session.commit()
        return db_article.id_article
