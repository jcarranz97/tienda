#!/usr/bin/python3
"""This module contains the shipping status model."""
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import func
from models import Base


class ShippingStatus(Base):
    """This class represents the shipping status model."""
    __tablename__ = 'shipping_statuses'

    id_status = Column(Integer, primary_key=True)
    status_name = Column("status_name", String, nullable=False)
    description = Column("description", String, nullable=False)
    created_at = Column(
        "created_at",
        DateTime,
        nullable=False,
        default=func.now(),  # pylint: disable=not-callable
    )
    updated_at = Column(
        "updated_at",
        DateTime,
        nullable=False,
        default=func.now(),  # pylint: disable=not-callable
        onupdate=func.now(),  # pylint: disable=not-callable
    )
