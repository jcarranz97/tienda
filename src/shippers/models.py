#!/usr/bin/python3
"""This module defines the models related to sellers."""
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship
from models import Base


class Shipper(Base):
    """User model"""
    __tablename__ = 'shippers'

    id_shipper = Column(Integer, primary_key=True)
    shipper_name = Column("shipper_name", String, nullable=False)

    # Relationships
    shipping_groups = relationship("ShippingGroup", back_populates="shipper")
