#!/usr/bin/python3
"""This module defines the models related to sellers."""
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Numeric
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from models import Base


class ArticleStatus(Base):
    __tablename__ = 'article_statuses'

    id_article_status = Column(Integer, primary_key=True, autoincrement=True)
    status_name = Column(String(255), nullable=False)

    # Relationships
    articles = relationship("Article", back_populates="article_status")


class Location(Base):
    __tablename__ = 'locations'

    id_location = Column(Integer, primary_key=True, autoincrement=True)
    location_name = Column(String(255), nullable=False)

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
    id_article_status = Column(
        Integer,
        ForeignKey('article_statuses.id_article_status'),
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
    article_status = relationship(
        "ArticleStatus",
        back_populates="articles",
    )
    location = relationship("Location", back_populates="articles")
    shipping_group = relationship("ShippingGroup", back_populates="articles")
