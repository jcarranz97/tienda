#!/usr/bin/env python
"""This module defines common queries for product management."""
from sqlalchemy import select
from sqlalchemy import func
from sqlalchemy.orm import aliased
from shipping.models import ShippingGroup
from . import models
from . import formulas




def get_product_query(
        session,
        product_id=None,
        id_shipping_group=None,
        shipping_label=None,
        ):
    """Get product query"""
    # Create an alias for the subquery counting products per shipping group
    subquery = select(
        models.product.id_shipping_group,
        func.count(models.product.id_product).label('product_count')  # pylint: disable=not-callable
    ).group_by(models.product.id_shipping_group).alias()

    # Create an alias to work with the subquery
    productCount = aliased(subquery)  # pylint: disable=invalid-name
    # Main query to fetch the required fields, including the "profit"
    # Main query using ORM models
    query = (
        session.query(
            models.product.id_product,
            models.product.description,
            models.product.shipping_label,
            models.product.purchase_price,
            ShippingGroup.shipping_group_name,
            models.productStatus.status_name,
            ShippingGroup.dollar_price,
            ShippingGroup.tax,
            ShippingGroup.shipping_cost,
            models.Location.location_name,
            # Calculate purchase_price_mxn using the helper function
            formulas.calculate_purchase_price_mxn(
                models.product,
                ShippingGroup,
                productCount,
            ),
            # Calculate profit using the helper function
            formulas.calculate_profit(
                models.product,
                formulas.calculate_purchase_price_mxn(
                    models.product,
                    ShippingGroup,
                    productCount,
                ),
            ),
            models.product.sale_price,
        )
        .join(ShippingGroup, models.product.id_shipping_group == ShippingGroup.id_shipping_group)
        .join(models.Location, models.product.id_location == models.Location.id_location)
        .join(productCount, models.product.id_shipping_group == productCount.c.id_shipping_group)
        .join(models.productStatus, models.product.id_product_status == models.productStatus.id_product_status)
    )

    # If product_id is provided, apply the filter
    if product_id:
        query = query.filter(models.product.id_product == product_id)

    # If shipping_group_name is provided, apply the filter
    if id_shipping_group:
        query = query.filter(models.product.id_shipping_group == id_shipping_group)

    # If shipping_label is provided, apply the filter
    if shipping_label:
        query = query.filter(models.product.shipping_label == shipping_label)

    return query


def get_product_status_by_name(session, status_name):
    """Get product status by name"""
    db_status = session.scalar(
        select(models.productStatus)
        .where(models.productStatus.status_name == status_name)
    )
    if not db_status:
        raise ValueError(
            f"Status '{status_name}' not found.")
    return db_status


def get_product_location_by_name(session, location_name):
    """Get product location by name"""
    db_location = session.scalar(
        select(models.Location)
        .where(models.Location.location_name == location_name)
    )
    if not db_location:
        raise ValueError(
            f"Location '{location_name}' not found.")
    return db_location
