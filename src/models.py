#!\usr\bin\python3
"""Models used in app

This module contains all models used in the app. This models are basically
classes that inherit from Base class and are used to create tables in the
database.

"""
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import DateTime
from sqlalchemy import Column
from sqlalchemy import func


class Base(DeclarativeBase):
    """Base class for all models"""

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
