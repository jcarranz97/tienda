#!/usr/bin/python3
"""This module defines formulas needed to article management."""
from sqlalchemy.sql.expression import case


def calculate_purchase_price_mxn(article, shipping_group, article_count_subquery):
    """
    Calculate the purchase price in MXN (purchase_price_mxn).
    """
    return (
        article.purchase_price * shipping_group.dollar_price * (1 + (shipping_group.tax * 0.01)) +
        (shipping_group.shipping_cost / article_count_subquery.c.article_count) * shipping_group.dollar_price
    ).label('purchase_price_mxn')


def calculate_profit(article, purchase_price_mxn):
    """
    Calculate profit if sale_price is not None, otherwise return None.
    """
    return case(
        (article.sale_price.is_(None), None),  # If sale_price is NULL, profit is NULL
        else_=article.sale_price - purchase_price_mxn
    ).label('profit')
