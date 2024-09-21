#!/usr/bin/env python
"""This module contains tasks for the shipping"""
from celery import shared_task
from sqlalchemy import select
from database import Session
from . import models
from . import schemas


@shared_task
def get_shipping_statuses():
    """Get shipping statuses from database"""
    with Session() as session:
        db_statuses = session.scalars(select(models.ShippingStatus)).all()
        statuses = [
            schemas.ShippingStatusBase(
                id=db_status.id_status,
                name=db_status.status_name,
                description=db_status.description,
                created_at=db_status.created_at,
                updated_at=db_status.updated_at,
            ).dict()
            for db_status in db_statuses
        ]
        return schemas.GetShippingStatusesResponse(statuses=statuses).dict()


@shared_task
def get_shipping_status(status_id: int):
    """Get shipping status from database"""
    with Session() as session:
        db_status = session.scalar(
            select(models.ShippingStatus)
            .where(models.ShippingStatus.id_status == status_id)
        )
        if not db_status:
            raise ValueError(f"Shipping status with ID {status_id} not found.")
        return schemas.ShippingStatusBase(
            id=db_status.id_status,
            name=db_status.status_name,
            description=db_status.description,
            created_at=db_status.created_at,
            updated_at=db_status.updated_at,
        ).dict()


@shared_task
def add_shipping_status(name: str, description: str):
    """Add shipping status to database"""
    with Session() as session:
        # Before adding a new shipping status, we should confirm that there is
        # no shipping status with the same name in the database. This is a
        # business rule that should be enforced.
        db_status = session.scalar(
            select(models.ShippingStatus)
            .where(models.ShippingStatus.status_name == name)
        )
        if db_status:
            raise ValueError(
                f"Shipping status '{name}' already exists in the database.")

        new_status = models.ShippingStatus(
            status_name=name,
            description=description,
        )
        session.add(new_status)
        session.commit()
        return new_status.id_status


@shared_task
def modify_shipping_status(status_id: int, name: str, description: str):
    """Modify shipping status by status_id"""
    with Session() as session:
        db_status = session.scalar(
            select(models.ShippingStatus)
            .where(models.ShippingStatus.id_status == status_id)
        )
        if not db_status:
            raise ValueError(f"Shipping status with ID {status_id} not found.")
        db_status.status_name = name
        db_status.description = description
        session.commit()
        return status_id


@shared_task
def delete_shipping_status(status_id: int):
    """Delete shipping status by status_id"""
    with Session() as session:
        db_status = session.scalar(
            select(models.ShippingStatus)
            .where(models.ShippingStatus.id_status == status_id)
        )
        if not db_status:
            raise ValueError(f"Shipping status with ID {status_id} not found.")
        session.delete(db_status)
        session.commit()
        return status_id
