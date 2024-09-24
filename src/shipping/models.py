#!/usr/bin/python3
"""This module contains the shipping status model."""
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import Numeric
from sqlalchemy import Text
from sqlalchemy.orm import relationship
from models import Base


class ShippingStatus(Base):
    """This class represents the shipping status model."""
    __tablename__ = 'shipping_statuses'

    id_status = Column(Integer, primary_key=True)
    status_name = Column("status_name", String, nullable=False)
    description = Column("description", String, nullable=False)

    # Relationships
    shipping_groups = relationship("ShippingGroup", back_populates="status")


class ShippingGroup(Base):
    """Shipping Group model"""
    __tablename__ = 'shipping_groups'

    id_shipping_group = Column(Integer, primary_key=True, autoincrement=True)
    shipping_group_name = Column(String(255), nullable=False)
    id_shipper = Column(
        Integer, ForeignKey('shippers.id_shipper'), nullable=False)
    id_status = Column(
        Integer, ForeignKey('shipping_statuses.id_status'), nullable=False)
    shipping_cost = Column(Numeric(10, 2), nullable=False)
    dollar_price = Column(Numeric(10, 2), nullable=False)
    tax = Column(Numeric(10, 2), nullable=False)
    notes = Column(Text, nullable=True)

    # Relationships
    shipper = relationship("Shipper", back_populates="shipping_groups")
    status = relationship("ShippingStatus", back_populates="shipping_groups")
    products = relationship("product", back_populates="shipping_group")
