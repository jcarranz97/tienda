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
        func.count(models.Product.id_product).label('product_count'),  # pylint: disable=not-callable
        func.sum(models.Product.purchase_price).label('total_price')   # Sum the purchase price
    ).group_by(models.Product.id_shipping_group).subquery()  # Here, we use .subquery() to create an explicit subquery

    # Main query to fetch the required fields, including the "profit"
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
            # Use subquery columns directly
            subquery.c.product_count,
            subquery.c.total_price,
            # Calculate shipping_cost using the helper function
            formulas.calculate_shipping_cost(
                ShippingGroup,
                subquery.c.total_price,
                models.Product.purchase_price,
            ),
            # Calculate purchase_price_mxn using the helper function
            formulas.calculate_purchase_price_mxn(
                models.Product,
                ShippingGroup,
                formulas.calculate_shipping_cost(
                    ShippingGroup,
                    subquery.c.total_price,
                    models.Product.purchase_price,
                ),
            ),
            # Calculate profit using the helper function
            formulas.calculate_profit(
                models.Product,
                formulas.calculate_purchase_price_mxn(
                    models.Product,
                    ShippingGroup,
                    formulas.calculate_shipping_cost(
                        ShippingGroup,
                        subquery.c.total_price,
                        models.Product.purchase_price,
                    ),
                ),
                formulas.calculate_mx_iva(16, models.Product.sale_price),
            ),
            models.Product.sale_price,
            formulas.calculate_mx_iva(16, models.Product.sale_price),
            formulas.calculate_profit_percentage(
                models.Product,
                formulas.calculate_purchase_price_mxn(
                    models.Product,
                    ShippingGroup,
                    formulas.calculate_shipping_cost(
                        ShippingGroup,
                        subquery.c.total_price,
                        models.Product.purchase_price,
                    ),
                ),
                formulas.calculate_profit(
                    models.Product,
                    formulas.calculate_purchase_price_mxn(
                        models.Product,
                        ShippingGroup,
                        formulas.calculate_shipping_cost(
                            ShippingGroup,
                            subquery.c.total_price,
                            models.Product.purchase_price,
                        ),
                    ),
                    formulas.calculate_mx_iva(16, models.Product.sale_price),
                ),
            ),
        )
        .join(ShippingGroup, models.Product.id_shipping_group == ShippingGroup.id_shipping_group)
        .join(models.Location, models.Product.id_location == models.Location.id_location)
        # Use the subquery directly in the join, referencing the appropriate column
        .outerjoin(subquery, models.Product.id_shipping_group == subquery.c.id_shipping_group)
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


def get_product_location_by_id(session, location_id):
    """Get product location by id"""
    db_location = session.scalar(
        select(models.Location)
        .where(models.Location.id_location == location_id)
    )
    if not db_location:
        raise ValueError(
            f"Location id '{location_id}' is not valid.")
    return db_location


def get_product_status_by_id(session, status_id):
    """Get product status by id"""
    db_status = session.scalar(
        select(models.ProductStatus)
        .where(models.ProductStatus.id_product_status == status_id)
    )
    if not db_status:
        raise ValueError(
            f"Status id '{status_id}' is not valid.")
    return db_status
