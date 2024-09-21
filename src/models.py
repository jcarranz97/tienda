#!\usr\bin\python3
"""Models used in app

This module contains all models used in the app. This models are basically
classes that inherit from Base class and are used to create tables in the
database.

"""
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all models"""
