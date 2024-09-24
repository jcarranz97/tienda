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
        models.Product.id_shipping_group,
        func.count(models.Product.id_product).label('product_count')  # pylint: disable=not-callable
    ).group_by(models.Product.id_shipping_group).alias()

    # Create an alias to work with the subquery
    ProductCount = aliased(subquery)  # pylint: disable=invalid-name
    # Main query to fetch the required fields, including the "profit"
    # Main query using ORM models
    query = (
        session.query(
            models.Product.id_product,
            models.Product.description,
            models.Product.shipping_label,
            models.Product.purchase_price,
            ShippingGroup.shipping_group_name,
            models.ProductStatus.status_name,
            ShippingGroup.dollar_price,
            ShippingGroup.tax,
            ShippingGroup.shipping_cost,
            models.Location.location_name,
            # Calculate purchase_price_mxn using the helper function
            formulas.calculate_purchase_price_mxn(
                models.Product,
                ShippingGroup,
                ProductCount,
            ),
            # Calculate profit using the helper function
            formulas.calculate_profit(
                models.Product,
                formulas.calculate_purchase_price_mxn(
                    models.Product,
                    ShippingGroup,
                    ProductCount,
                ),
            ),
            models.Product.sale_price,
        )
        .join(ShippingGroup, models.Product.id_shipping_group == ShippingGroup.id_shipping_group)
        .join(models.Location, models.Product.id_location == models.Location.id_location)
        .join(ProductCount, models.Product.id_shipping_group == ProductCount.c.id_shipping_group)
        .join(models.ProductStatus, models.Product.id_product_status == models.ProductStatus.id_product_status)
    )

    # If product_id is provided, apply the filter
    if product_id:
        query = query.filter(models.Product.id_product == product_id)

    # If shipping_group_name is provided, apply the filter
    if id_shipping_group:
        query = query.filter(models.Product.id_shipping_group == id_shipping_group)

    # If shipping_label is provided, apply the filter
    if shipping_label:
        query = query.filter(models.Product.shipping_label == shipping_label)

    return query


def get_product_status_by_name(session, status_name):
    """Get product status by name"""
    db_status = session.scalar(
        select(models.ProductStatus)
        .where(models.ProductStatus.status_name == status_name)
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
