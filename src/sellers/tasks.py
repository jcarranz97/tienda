#!/usr/bin/env python
"""Celery tasks related to sellers."""
from time import sleep
from celery import shared_task
from sqlalchemy import select
from database import engine
from database import Session
from . import models
from . import schemas


@shared_task
def add(a: int, b: int):
    """Add two numbers and return the result.

    Args:
        a (int): The first number.
        b (int): The second number.

    Returns:
        dict: The result of the addition.
    """
    for i in range(a, b):
        print(i)
        sleep(1)
    return {"number": a + b}


@shared_task
def get_sellers():
    """Get sellers from database"""
    # Get sellers should return GetSellersResponse, which is a schema defined
    # as a Pydantic model in schemas.py. This schema has a list of SellerBase
    # objects.
    with Session() as session:
        db_sellers = session.scalars(select(models.Seller)).all()
        sellers = [
            schemas.SellerBase(
                id=db_seller.id_seller,
                name=db_seller.seller_name,
                created_at=db_seller.created_at,
                updated_at=db_seller.updated_at,
            ).dict()
            for db_seller in db_sellers
        ]
        return schemas.GetSellersResponse(sellers=sellers).dict()


@shared_task
def get_seller(seller_id: int):
    """Get seller from database"""
    with Session() as session:
        db_seller = session.scalar(
            select(models.Seller).where(models.Seller.id_seller == seller_id)
        )
        if not db_seller:
            raise ValueError(f"Seller with ID {seller_id} not found.")
        return schemas.SellerBase(
            id=db_seller.id_seller,
            name=db_seller.seller_name,
            created_at=db_seller.created_at,
            updated_at=db_seller.updated_at,
        ).dict()


@shared_task
def add_seller(name: str):
    """Add seller to database"""
    with Session() as session:
        # Before adding a new seller, we should confirm that there is no seller
        # with the same name in the database. This is a business rule that
        # should be enforced.
        db_seller = session.scalar(
            select(models.Seller).where(models.Seller.seller_name == name)
        )
        if db_seller:
            raise ValueError(
                f"Seller '{name}' already exists in the database.")

        new_seller = models.Seller(seller_name=name)
        session.add(new_seller)
        session.commit()
        return schemas.AddSellerResponse(id=new_seller.id_seller).dict()


@shared_task
def update_seller(seller_id: int, seller_name: str):
    """Update seller by seller_id"""
    with Session() as session:
        db_seller = session.scalar(
            select(models.Seller).where(models.Seller.id_seller == seller_id)
        )
        if not db_seller:
            raise ValueError(f"Seller with ID {seller_id} not found.")
        db_seller.seller_name = seller_name
        session.commit()
        return seller_id


@shared_task
def delete_seller(seller_id: int):
    """Delete seller by seller_id"""
    with Session() as session:
        db_seller = session.scalar(
            select(models.Seller).where(models.Seller.id_seller == seller_id)
        )
        if not db_seller:
            raise ValueError(f"Seller with ID {seller_id} not found.")
        session.delete(db_seller)
        session.commit()
        return seller_id
