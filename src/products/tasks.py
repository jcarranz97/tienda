#!/usr/bin/env python
"""Celery tasks related to products."""
from celery import shared_task
from sqlalchemy import select
from database import Session
from shipping.queries import get_shipping_group_by_name
from shipping.queries import get_shipping_group_by_id
from . import models
from . import schemas
from . import queries


@shared_task
def get_product_statuses():
    """Get product statuses from database"""
    with Session() as session:
        db_statuses = session.scalars(select(models.ProductStatus)).all()
        statuses = [
            schemas.ProductStatusBase(
                id=db_status.id_product_status,
                name=db_status.status_name,
                created_at=db_status.created_at,
                updated_at=db_status.updated_at,
            ).dict()
            for db_status in db_statuses
        ]
        return schemas.GetproductsStatusesResponse(statuses=statuses).dict()


@shared_task
def get_product_status(id_product_status: int):
    """Get product status from database"""
    with Session() as session:
        db_status = session.scalar(
            select(models.ProductStatus)
            .where(
                models.ProductStatus.id_product_status == id_product_status
            )
        )
        if not db_status:
            raise ValueError(
                f"product status with ID {id_product_status} not found.")
        return schemas.ProductStatusBase(
            id=db_status.id_product_status,
            name=db_status.status_name,
            created_at=db_status.created_at,
            updated_at=db_status.updated_at,
        ).dict()


@shared_task
def add_product_status(name: str):
    """Add product status to database"""
    with Session() as session:
        # Before adding a new status, we should confirm that there is no status
        # with the same name in the database. This is a business rule that
        # should be enforced.
        db_status = session.scalar(
            select(models.ProductStatus)
            .where(models.ProductStatus.status_name == name)
        )
        if db_status:
            raise ValueError(
                f"product status '{name}' already exists in the database.")

        new_status = models.ProductStatus(status_name=name)
        session.add(new_status)
        session.commit()
        return new_status.id_product_status


@shared_task
def update_product_status(id_product_status: int, name: str):
    """Update product status by id_product_status"""
    with Session() as session:
        db_status = session.scalar(
            select(models.ProductStatus)
            .where(models.ProductStatus.id_product_status == id_product_status)
        )
        if not db_status:
            raise ValueError(
                f"product status with ID {id_product_status} not found.")
        db_status.status_name = name
        session.commit()
        return id_product_status


@shared_task
def delete_product_status(id_product_status: int):
    """Delete product status by id_product_status"""
    with Session() as session:
        db_status = session.scalar(
            select(models.ProductStatus)
            .where(models.ProductStatus.id_product_status == id_product_status)
        )
        if not db_status:
            raise ValueError(
                f"product status with ID {id_product_status} not found.")
        session.delete(db_status)
        session.commit()
        return id_product_status


@shared_task
def get_locations():
    """Get locations from database"""
    with Session() as session:
        db_locations = session.scalars(select(models.Location)).all()
        locations = [
            schemas.LocationBase(
                id=db_location.id_location,
                name=db_location.location_name,
                created_at=db_location.created_at,
                updated_at=db_location.updated_at,
            ).dict()
            for db_location in db_locations
        ]
        return schemas.GetLocationsResponse(locations=locations).dict()


@shared_task
def get_location(location_id: int):
    """Get location from database"""
    with Session() as session:
        db_location = session.scalar(
            select(models.Location)
            .where(models.Location.id_location == location_id)
        )
        if not db_location:
            raise ValueError(f"Location with ID {location_id} not found.")
        return schemas.LocationBase(
            id=db_location.id_location,
            name=db_location.location_name,
            created_at=db_location.created_at,
            updated_at=db_location.updated_at,
        ).dict()


@shared_task
def add_location(name: str):
    """Add location to database"""
    with Session() as session:
        # Before adding a new location, we should confirm that there is no
        # location with the same name in the database. This is a business rule
        # that should be enforced.
        db_location = session.scalar(
            select(models.Location)
            .where(models.Location.location_name == name)
        )
        if db_location:
            raise ValueError(
                f"Location '{name}' already exists in the database.")

        new_location = models.Location(location_name=name)
        session.add(new_location)
        session.commit()
        return new_location.id_location


@shared_task
def update_location(location_id: int, name: str):
    """Update location by location_id"""
    with Session() as session:
        db_location = session.scalar(
            select(models.Location)
            .where(models.Location.id_location == location_id)
        )
        if not db_location:
            raise ValueError(f"Location with ID {location_id} not found.")
        db_location.location_name = name
        session.commit()
        return location_id


@shared_task
def delete_location(location_id: int):
    """Delete location by location_id"""
    with Session() as session:
        db_location = session.scalar(
            select(models.Location)
            .where(models.Location.id_location == location_id)
        )
        if not db_location:
            raise ValueError(f"Location with ID {location_id} not found.")
        session.delete(db_location)
        session.commit()
        return location_id


@shared_task
def get_products(
        shipping_group_name: str | None = None,
        shipping_label: str | None = None,
        ):
    """Get products from database"""
    with Session() as session:
        # Before fetching the products, we need to confirm that
        # shipping_group_name is valid (If entered),
        db_shipping_group = None  # Initialize as None

        if shipping_group_name:
            db_shipping_group = get_shipping_group_by_name(
                session=session,
                shipping_group_name=shipping_group_name,
            )
        # Main query to fetch the required fields, including the "profit"
        query = queries.get_product_query(
            session=session,
            id_shipping_group=db_shipping_group.id_shipping_group if shipping_group_name else None,
            shipping_label=shipping_label,
        )

        products = [
            schemas.ProductDetailResponse(
                id_product=db_product.id_product,
                description=db_product.description,
                shipping_label=db_product.shipping_label,
                purchase_price=db_product.purchase_price,
                shipping_group=db_product.shipping_group_name,
                status=db_product.status_name,
                location_name=db_product.location_name,
                purchase_price_mxn=db_product.purchase_price_mxn,
                invoice_id=db_product.id_invoice,
                mx_iva=db_product.mx_iva,
                sale_price=db_product.sale_price,
                shipping_cost=db_product.shipping_cost,
                profit=db_product.profit,
                profit_percentage=db_product.profit_percentage,
            ).dict()
            for db_product in query.all()
        ]
        return schemas.GetProductsDetailResponse(
            products=products,
            num_products=len(products),
        ).dict()


@shared_task
def get_product(product_id: int):
    """Get product from database"""
    # Same as get_products, but with a filter by product_id in the query
    with Session() as session:
        query = queries.get_product_query(session, product_id)

        if not (db_product := query.first()):
            raise ValueError(f"product with ID {product_id} not found.")

        return schemas.ProductDetailResponse(
            id_product=db_product.id_product,
            description=db_product.description,
            shipping_label=db_product.shipping_label,
            purchase_price=db_product.purchase_price,
            shipping_group=db_product.shipping_group_name,
            status=db_product.status_name,
            location_name=db_product.location_name,
            purchase_price_mxn=db_product.purchase_price_mxn,
            invoice_id=db_product.id_invoice,
            mx_iva=db_product.mx_iva,
            profit=db_product.profit,
            profit_percentage=db_product.profit_percentage,
            sale_price=db_product.sale_price,
            shipping_cost=db_product.shipping_cost,
        ).dict()


@shared_task
def add_product_with_ids(
    description: str,
    shipping_label: str,
    purchase_price: float,
    product_location_id: int,
    product_status_id: int,
    shipping_group_id: int | None = None,
):
    """Add product to database by using IDs"""
    # Put shipping_label in lowercase
    shipping_label = shipping_label.lower()
    with Session() as session:
        # Initalizing db_shipping_group as None
        product_location = queries.get_product_location_by_id(
            session=session,
            location_id=product_location_id,
        )
        product_status = queries.get_product_status_by_id(
            session=session,
            status_id=product_status_id,
        )
        db_shipping_group = None
        if shipping_group_id:
            db_shipping_group = get_shipping_group_by_id(
                session=session,
                shipping_group_id=shipping_group_id,
            )
        new_product = models.Product(
            description=description,
            shipping_label=shipping_label,
            purchase_price=purchase_price,
            id_product_status=product_status.id_product_status,
            id_location=product_location.id_location,
            id_shipping_group=db_shipping_group.id_shipping_group if shipping_group_id else None,
        )
        session.add(new_product)
        session.commit()
        return new_product.id_product


@shared_task
def update_product(
    product_id: int,
    description: str | None = None,
    shipping_label: str | None = None,
    purchase_price: float | None = None,
    sale_price: float | None = None,
    id_product_status: int | None = None,
    id_location: int | None = None,
    id_shipping_group: int | None = None,
):
    """Update product by product_id"""
    with Session() as session:
        db_product = session.scalar(
            select(models.Product)
            .where(models.Product.id_product == product_id)
        )
        if not db_product:
            raise ValueError(f"product with ID {product_id} not found.")
        # Only update the fields that are not None in the request.
        # If all fields are None, the product will not be updated. This is
        # should trigger a validation error in the API.
        item_modifications = 0
        if description is not None:
            db_product.description = description
            item_modifications += 1
        if shipping_label is not None:
            db_product.shipping_label = shipping_label
            item_modifications += 1
        if purchase_price is not None:
            db_product.purchase_price = purchase_price
            item_modifications += 1
        if sale_price is not None:
            db_product.sale_price = sale_price
            item_modifications += 1
        if id_product_status is not None:
            db_product.id_product_status = id_product_status
            item_modifications += 1
        if id_location is not None:
            db_product.id_location = id_location
            item_modifications += 1
        if id_shipping_group is not None:
            db_product.id_shipping_group = id_shipping_group
            item_modifications += 1
        if item_modifications == 0:
            raise ValueError("No fields to update.")
        session.commit()
        return schemas.UpdateproductResponse(
            id=product_id, updated_items=item_modifications
        ).dict()


@shared_task
def delete_product(product_id: int):
    """Delete product by product_id"""
    with Session() as session:
        db_product = session.scalar(
            select(models.Product)
            .where(models.Product.id_product == product_id)
        )
        if not db_product:
            raise ValueError(f"product with ID {product_id} not found.")
        session.delete(db_product)
        session.commit()
        return product_id


@shared_task
def add_sale_price(
        shipping_group_name: str,
        shipping_label: str,
        sale_price: float,
) -> int:
    """Add sale price to database"""
    with Session() as session:
        # Before adding a new sale price, we should confirm that the
        # shipping_group_name is valid.
        db_shipping_group = get_shipping_group_by_name(
            session=session,
            shipping_group_name=shipping_group_name,
        )

        db_product = session.scalar(
            select(models.Product)
            .where(
                models.Product.shipping_label == shipping_label,
                models.Product.id_shipping_group == db_shipping_group.id_shipping_group
            )
        )
        if not db_product:
            raise ValueError(
                f"product with shipping label '{shipping_label}' not found " +
                "in the shipping group '{shipping_group_name}'.")
        db_product.sale_price = sale_price
        session.commit()
        return db_product.id_product


@shared_task
def add_sale_price_with_id(
        id_product: int,
        sale_price: float,
) -> int:
    """Add sale price to database by product_id"""
    with Session() as session:
        db_product = session.scalar(
            select(models.Product)
            .where(models.Product.id_product == id_product)
        )
        if not db_product:
            raise ValueError(f"product with ID {id_product} not found.")
        db_product.sale_price = sale_price
        session.commit()
        return db_product.id_product


@shared_task
def add_sale_price_with_id_2(
        id_product: int,
        sale_price: float,
        ) -> schemas.ProductDetailResponse:
    """Add sale price to database by product_id"""
    with Session() as session:
        db_product = session.scalar(
            select(models.Product)
            .where(models.Product.id_product == id_product)
        )
        if not db_product:
            raise ValueError(f"product with ID {id_product} not found.")
        db_product.sale_price = sale_price
        session.commit()
        # Return the product using the query get_function_query
        query = queries.get_product_query(session, id_product)
        db_product = query.first()
        return schemas.ProductDetailResponse(
            id_product=db_product.id_product,
            description=db_product.description,
            shipping_label=db_product.shipping_label,
            purchase_price=db_product.purchase_price,
            shipping_group=db_product.shipping_group_name,
            status=db_product.status_name,
            location_name=db_product.location_name,
            purchase_price_mxn=db_product.purchase_price_mxn,
            invoice_id=db_product.id_invoice,
            mx_iva=db_product.mx_iva,
            profit=db_product.profit,
            profit_percentage=db_product.profit_percentage,
            sale_price=db_product.sale_price,
            shipping_cost=db_product.shipping_cost,
        ).dict()
