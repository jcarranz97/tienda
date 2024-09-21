#!/usr/bin/python3
"""This module defines the models related to sellers."""
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import func
from sqlalchemy import Numeric
from sqlalchemy import Text
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from models import Base


class ArticleAvailability(Base):
    __tablename__ = 'article_availability'

    id_availability = Column(Integer, primary_key=True, autoincrement=True)
    availability_name = Column(String(255), nullable=False)
    # pylint: disable=not-callable
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    articles = relationship("Article", back_populates="availability")


class Location(Base):
    __tablename__ = 'locations'

    id_location = Column(Integer, primary_key=True, autoincrement=True)
    location_name = Column(String(255), nullable=False)
    # pylint: disable=not-callable
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    articles = relationship("Article", back_populates="location")


class Article(Base):
    """Article model"""
    __tablename__ = 'articles'

    id_article = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(255), nullable=False)
    shipping_label = Column(String(255), nullable=False)
    purchase_price = Column(Numeric(10, 2), nullable=False)
    sale_price = Column(Numeric(10, 2), nullable=False)
    id_availability = Column(
        Integer,
        ForeignKey('article_availability.id_availability'),
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

    # pylint: disable=not-callable
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    availability = relationship(
        "ArticleAvailability",
        back_populates="articles",
    )
    location = relationship("Location", back_populates="articles")
    shipping_group = relationship("ShippingGroup", back_populates="articles")
