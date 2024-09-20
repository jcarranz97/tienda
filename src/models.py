#!\usr\bin\python3
"""Models used in app"""
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all models"""


class Seller(Base):
    """User model"""
    __tablename__ = 'sellers'

    id_seller = Column(Integer, primary_key=True)
    name = Column("seller_name", String, nullable=False)
