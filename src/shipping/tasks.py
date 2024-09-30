#!/usr/bin/env python
"""This module contains tasks for the shipping"""
from celery import shared_task
from sqlalchemy import select
from database import Session
from shippers.models import Shipper
from products.models import Product
from sqlalchemy import func
from . import models
from . import schemas
from . import queries


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
def update_shipping_status(status_id: int, name: str, description: str):
    """Update shipping status by status_id"""
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
    """Get shipping groups from the database with the number of products in each group"""
    with Session() as session:
        # Use the reusable query to get all shipping groups
        db_groups = queries.get_shipping_group_query(session).all()

        # Construct the response for all groups
        groups = [
            schemas.ShippingGroupBase(
                id=db_group.ShippingGroup.id_shipping_group,
                name=db_group.ShippingGroup.shipping_group_name,
                shipper=db_group.ShippingGroup.shipper.shipper_name,
                status=db_group.ShippingGroup.status.status_name,
                shipping_cost=db_group.ShippingGroup.shipping_cost,
                dollar_price=db_group.ShippingGroup.dollar_price,
                tax=db_group.ShippingGroup.tax,
                created_at=db_group.ShippingGroup.created_at,
                updated_at=db_group.ShippingGroup.updated_at,
                num_products=db_group.num_products,
                notes=db_group.ShippingGroup.notes,
            ).dict()
            for db_group in db_groups
        ]

        return schemas.GetShippingGroupsResponse(
            groups=groups,
            num_groups=len(groups),
        ).dict()


@shared_task
def get_shipping_group(group_id: int):
    """Get shipping group from database"""
    with Session() as session:
        # Use the reusable query to get a specific shipping group
        db_group = queries.get_shipping_group_query(
            session,
            shipping_group_id=group_id
        ).first()

        # If no group found, return None or handle as appropriate
        if db_group is None:
            return None

        # Construct the response for the found shipping group
        group = schemas.ShippingGroupBase(
            id=db_group.ShippingGroup.id_shipping_group,
            name=db_group.ShippingGroup.shipping_group_name,
            shipper=db_group.ShippingGroup.shipper.shipper_name,
            status=db_group.ShippingGroup.status.status_name,
            shipping_cost=db_group.ShippingGroup.shipping_cost,
            dollar_price=db_group.ShippingGroup.dollar_price,
            tax=db_group.ShippingGroup.tax,
            created_at=db_group.ShippingGroup.created_at,
            updated_at=db_group.ShippingGroup.updated_at,
            num_products=db_group.num_products,
            notes=db_group.ShippingGroup.notes,
        )

        return group.dict()


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


@shared_task
def update_shipping_group(
        id_shipping_group: int,
        name: str | None = None,
        id_shipper: int | None = None,
        id_status: int | None = None,
        shipping_cost: float | None = None,
        dollar_price: float | None = None,
        tax: float | None = None,
        notes: str | None = None,
        ) -> schemas.UpdateShippingGroupResponse:
    """Update shipping group by id_shipping_group.

    This task updates the shipping group with the given id_shipping_group. All
    fields are optional, so only the fields that are not None will be updated.

    Returns:
        UpdateShippingGroupResponse: The response object with the ID of the
            updated shipping group and the number of changes made.
    """
    with Session() as session:
        db_group = session.scalar(
            select(models.ShippingGroup)
            .where(models.ShippingGroup.id_shipping_group == id_shipping_group)
        )
        if not db_group:
            raise ValueError(
                f"Shipping group with ID {id_shipping_group} not found.")

        num_changes = 0
        # Update the fields that are not None
        if name is not None:
            db_group.shipping_group_name = name
            num_changes += 1
        if id_shipper is not None:
            db_group.id_shipper = id_shipper
            num_changes += 1
        if id_status is not None:
            db_group.id_status = id_status
            num_changes += 1
        if shipping_cost is not None:
            db_group.shipping_cost = shipping_cost
            num_changes += 1
        if dollar_price is not None:
            db_group.dollar_price = dollar_price
            num_changes += 1
        if tax is not None:
            db_group.tax = tax
            num_changes += 1
        if notes is not None:
            db_group.notes = notes
            num_changes += 1

        if not num_changes:
            raise ValueError("No changes to update.")

        session.commit()
        return schemas.UpdateShippingGroupResponse(
            id=id_shipping_group,
            num_changes=num_changes,
        ).dict()


@shared_task
def delete_shipping_group(id_shipping_group: int):
    """Delete shipping group by id_shipping_group"""
    with Session() as session:
        db_group = session.scalar(
            select(models.ShippingGroup)
            .where(models.ShippingGroup.id_shipping_group == id_shipping_group)
        )
        if not db_group:
            raise ValueError(
                f"Shipping group with ID {id_shipping_group} not found.")
        session.delete(db_group)
        session.commit()
        return id_shipping_group
