#!/usr/bin/python3
"""This module defines the models related to sellers."""
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import func
from models import Base
from sqlalchemy.orm import relationship


class Shipper(Base):
    """User model"""
    __tablename__ = 'shippers'

    id_shipper = Column(Integer, primary_key=True)
    shipper_name = Column("shipper_name", String, nullable=False)
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

    # Relationships
    shipping_groups = relationship("ShippingGroup", back_populates="shipper")
