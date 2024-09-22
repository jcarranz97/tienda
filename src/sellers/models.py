#!/usr/bin/python3
"""This module defines the models related to sellers."""
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from models import Base


class Seller(Base):
    """User model"""
    __tablename__ = 'sellers'

    id_seller = Column(Integer, primary_key=True)
    seller_name = Column("seller_name", String, nullable=False)
