#!/usr/bin/env python
"""This module defines common queries for product management."""
from sqlalchemy import func
from sqlalchemy import select
from products.models import Product
from . import models


def get_shipping_group_by_name(session, shipping_group_name):
    """Get shipping group by name"""
    db_shipping_group = session.scalar(
        select(models.ShippingGroup)
        .where(models.ShippingGroup.shipping_group_name == shipping_group_name)
    )
    if not db_shipping_group:
        raise ValueError(
            f"Shipping group '{shipping_group_name}' not found.")
    return db_shipping_group


def get_shipping_group_by_id(session, shipping_group_id):
    """Get shipping group by id"""
    db_shipping_group = session.scalar(
        select(models.ShippingGroup)
        .where(models.ShippingGroup.id_shipping_group == shipping_group_id)
    )
    if not db_shipping_group:
        raise ValueError(
            f"Shipping group id '{shipping_group_id}' is not valid.")
    return db_shipping_group


def get_shipping_group_query(session, shipping_group_id=None):
    """Construct a query to get shipping groups with the number of products in each group"""
    subquery = (
        session.query(
            Product.id_shipping_group,
            func.count(Product.id_product).label('num_products')  # pylint: disable=not-callable
        )
        .group_by(Product.id_shipping_group)
        .subquery()
    )

    # Create the base query to join ShippingGroup with the subquery to get the product count
    query = (
        session.query(
            models.ShippingGroup,
            func.coalesce(subquery.c.num_products, 0).label('num_products')
        )
        .outerjoin(subquery, models.ShippingGroup.id_shipping_group == subquery.c.id_shipping_group)
    )

    # If shipping_group_id is provided, add a filter for it
    if shipping_group_id is not None:
        query = query.filter(models.ShippingGroup.id_shipping_group == shipping_group_id)

    return query
