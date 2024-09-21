#!/usr/bin/env python
"""Celery tasks related to group2."""
from celery import shared_task
from sqlalchemy import select
from database import Session
from . import models
from . import schemas


@shared_task
def get_shippers():
    """Get shippers from database"""
    with Session() as session:
        db_shippers = session.scalars(select(models.Shipper)).all()
        shippers = [
            schemas.ShipperBase(
                id=db_shipper.id_shipper,
                name=db_shipper.name,
                created_at=db_shipper.created_at,
                updated_at=db_shipper.updated_at,
            ).dict()
            for db_shipper in db_shippers
        ]
        return schemas.GetShippersResponse(shippers=shippers).dict()


@shared_task
def get_shipper(shipper_id: int):
    """Get shipper from database"""
    with Session() as session:
        db_shipper = session.scalar(
            select(models.Shipper)
            .where(models.Shipper.id_shipper == shipper_id)
        )
        if not db_shipper:
            raise ValueError(f"Shipper with ID {shipper_id} not found.")
        return schemas.ShipperBase(
            id=db_shipper.id_shipper,
            name=db_shipper.name,
            created_at=db_shipper.created_at,
            updated_at=db_shipper.updated_at,
        ).dict()


@shared_task
def add_shipper(name: str):
    """Add shipper to database"""
    with Session() as session:
        # Before adding a new shipper, we should confirm that there is no
        # shipper with the same name in the database. This is a business rule
        # that should be enforced.
        db_shipper = session.scalar(
            select(models.Shipper).where(models.Shipper.name == name)
        )
        if db_shipper:
            raise ValueError(
                f"Shipper '{name}' already exists in the database.")

        new_shipper = models.Shipper(name=name)
        session.add(new_shipper)
        session.commit()
        return new_shipper.id_shipper


@shared_task
def modify_shipper(shipper_id: int, name: str):
    """Modify shipper by shipper_id"""
    with Session() as session:
        db_shipper = session.scalar(
            select(models.Shipper)
            .where(models.Shipper.id_shipper == shipper_id)
        )
        if not db_shipper:
            raise ValueError(f"Shipper with ID {shipper_id} not found.")
        db_shipper.name = name
        session.commit()
        return shipper_id


@shared_task
def delete_shipper(shipper_id: int):
    """Delete shipper by shipper_id"""
    with Session() as session:
        db_shipper = session.scalar(
            select(models.Shipper)
            .where(models.Shipper.id_shipper == shipper_id)
        )
        if not db_shipper:
            raise ValueError(f"Shipper with ID {shipper_id} not found.")
        session.delete(db_shipper)
        session.commit()
        return shipper_id
