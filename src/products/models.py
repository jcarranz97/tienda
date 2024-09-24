#!/usr/bin/python3
"""This module defines the models related to sellers."""
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Numeric
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from models import Base


class productStatus(Base):
    """productStatus model"""
    __tablename__ = 'product_statuses'

    id_product_status = Column(Integer, primary_key=True, autoincrement=True)
    status_name = Column(String(255), nullable=False)

    # Relationships
    products = relationship("product", back_populates="product_status")


class Location(Base):
    """Location model"""
    __tablename__ = 'locations'

    id_location = Column(Integer, primary_key=True, autoincrement=True)
    location_name = Column(String(255), nullable=False)

    # Relationships
    products = relationship("product", back_populates="location")


class product(Base):
    """product model"""
    __tablename__ = 'products'

    id_product = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(255), nullable=False)
    shipping_label = Column(String(255), nullable=False)
    purchase_price = Column(Numeric(10, 2), nullable=False)
    sale_price = Column(Numeric(10, 2), nullable=False)
    id_product_status = Column(
        Integer,
        ForeignKey('product_statuses.id_product_status'),
        nullable=False,
    )
    id_location = Column(
        Integer,
        ForeignKey('locations.id_location'),
        nullable=False,
    )
    id_shipping_group = Column(
        Integer,
        ForeignKey('shipping_groups.id_shipping_group'),
        nullable=True,
    )

    # Relationships
    product_status = relationship(
        "productStatus",
        back_populates="products",
    )
    location = relationship("Location", back_populates="products")
    shipping_group = relationship("ShippingGroup", back_populates="products")
