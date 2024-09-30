#!/usr/bin/python3
"""This module defines formulas needed to product management."""
from sqlalchemy.sql.expression import case
from sqlalchemy.sql import func


def calculate_shipping_cost(shipping_group, total_price, purchase_price):
    """
    Calculate the shipping cost in MXN (shipping_cost_mxn).
    """
    return (
        func.round(
            (shipping_group.shipping_cost / func.coalesce(total_price, 1)) * purchase_price,
            2  # Round to 2 decimal places
        )
    ).label('shipping_cost')


def calculate_purchase_price_mxn(product, shipping_group, shipping_cost_mxn):
    """
    Calculate the purchase price in MXN (purchase_price_mxn).
    """
    return (
        func.round(
            product.purchase_price * shipping_group.dollar_price * (1 + (shipping_group.tax * 0.01)) +
            shipping_cost_mxn,
            2  # Round to 2 decimal places
        )
    ).label('purchase_price_mxn')


def calculate_profit(product, purchase_price_mxn):
    """
    Calculate profit if sale_price is not None, otherwise return None.
    """
    return case(
        (product.sale_price.is_(None), None),  # If sale_price is NULL, profit is NULL
        else_=product.sale_price - purchase_price_mxn
    ).label('profit')
