#!/usr/bin/env python
"""This module defines common queries for article management."""
from sqlalchemy import select
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
