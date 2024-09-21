#!/usr/bin/env python
"""This module contains tasks for the shipping"""
from celery import shared_task
from sqlalchemy import select
from database import Session
from shippers.models import Shipper
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


@shared_task
def get_shipping_groups():
    """Get shipping groups from database"""
    with Session() as session:
        db_groups = session.scalars(select(models.ShippingGroup)).all()
        groups = [
            schemas.ShippingGroupBase(
                id=db_group.id_shipping_group,
                name=db_group.shipping_group_name,
                id_shipper=db_group.id_shipper,
                id_status=db_group.id_status,
                shipping_cost=db_group.shipping_cost,
                dollar_price=db_group.dollar_price,
                tax=db_group.tax,
                created_at=db_group.created_at,
                updated_at=db_group.updated_at,
                notes=db_group.notes,
            ).dict()
            for db_group in db_groups
        ]
        return schemas.GetShippingGroupsResponse(groups=groups).dict()


@shared_task
def get_shipping_group(group_id: int):
    """Get shipping group from database"""
    with Session() as session:
        db_group = session.scalar(
            select(models.ShippingGroup)
            .where(models.ShippingGroup.id_shipping_group == group_id)
        )
        if not db_group:
            raise ValueError(f"Shipping group with ID {group_id} not found.")
        return schemas.ShippingGroupBase(
            id=db_group.id_shipping_group,
            name=db_group.shipping_group_name,
            id_shipper=db_group.id_shipper,
            id_status=db_group.id_status,
            shipping_cost=db_group.shipping_cost,
            dollar_price=db_group.dollar_price,
            tax=db_group.tax,
            created_at=db_group.created_at,
            updated_at=db_group.updated_at,
            notes=db_group.notes,
        ).dict()


# pylint: disable=too-many-arguments
@shared_task
def add_shipping_group(
        name: str,
        id_shipper: int,
        id_status: int,
        shipping_cost: float,
        dollar_price: float,
        tax: float,
        notes: str | None,
):
    """Add shipping group to database"""
    with Session() as session:
        # Before adding a new shipping group, we should confirm that there is
        # no shipping group with the same name in the database. This is a
        # business rule that should be enforced.
        db_group = session.scalar(
            select(models.ShippingGroup)
            .where(models.ShippingGroup.shipping_group_name == name)
        )
        if db_group:
            raise ValueError(
                f"Shipping group '{name}' already exists in the database.")


        # Check if the shipper and status exist
        db_shipper = session.scalar(
            select(Shipper).where(Shipper.id_shipper == id_shipper)
        )
        if not db_shipper:
            raise ValueError(f"Shipper with ID {id_shipper} not found.")
        db_status = session.scalar(
            select(models.ShippingStatus)
            .where(models.ShippingStatus.id_status == id_status)
        )
        if not db_status:
            raise ValueError(f"Shipping status with ID {id_status} not found.")

        # Add the new shipping group
        new_group = models.ShippingGroup(
            shipping_group_name=name,
            id_shipper=id_shipper,
            id_status=id_status,
            shipping_cost=shipping_cost,
            dollar_price=dollar_price,
            tax=tax,
            notes=notes,
        )
        session.add(new_group)
        session.commit()
        return new_group.id_shipping_group
