#!/usr/bin/env python
"""This module defines common queries for article management."""
from sqlalchemy import select
from sqlalchemy import func
from sqlalchemy.orm import aliased
from shipping.models import ShippingGroup
from . import models
from . import formulas


def get_article_query(session, article_id=None, id_shipping_group=None):
    """Get article query"""
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

    # Main query to fetch the required fields, including the "profit"
    # Main query using ORM models
    query = (
        session.query(
            models.Article.id_article,
            models.Article.description,
            models.Article.shipping_label,
            models.Article.purchase_price,
            ShippingGroup.shipping_group_name,
            models.ArticleStatus.status_name,
            ShippingGroup.dollar_price,
            ShippingGroup.tax,
            ShippingGroup.shipping_cost,
            models.Location.location_name,
            # Calculate purchase_price_mxn using the helper function
            formulas.calculate_purchase_price_mxn(
                models.Article,
                ShippingGroup,
                ArticleCount,
            ),
            # Calculate profit using the helper function
            formulas.calculate_profit(
                models.Article,
                formulas.calculate_purchase_price_mxn(
                    models.Article,
                    ShippingGroup,
                    ArticleCount,
                ),
            ),
            models.Article.sale_price,
        )
        .join(ShippingGroup, models.Article.id_shipping_group == ShippingGroup.id_shipping_group)
        .join(models.Location, models.Article.id_location == models.Location.id_location)
        .join(ArticleCount, models.Article.id_shipping_group == ArticleCount.c.id_shipping_group)
        .join(models.ArticleStatus, models.Article.id_article_status == models.ArticleStatus.id_article_status)
    )

    # If article_id is provided, apply the filter
    if article_id:
        query = query.filter(models.Article.id_article == article_id)

    # If shipping_group_name is provided, apply the filter
    if id_shipping_group:
        query = query.filter(models.Article.id_shipping_group == id_shipping_group)

    return query
