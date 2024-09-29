#!/usr/bin/env python
"""Router for the API for product management."""
from fastapi import APIRouter
from . import schemas
from . import tasks

router = APIRouter()


@router.get("/get-products-statuses")
async def get_products_statuses() -> schemas.GetproductsStatusesResponse:
    """Get all products statuses"""
    task = tasks.get_product_statuses.delay()
    return task.get()


@router.get("/get-product-status/{id_product_status}")
async def get_product_status(id_product_status: int) -> schemas.ProductStatusBase:
    """Get an product status"""
    task = tasks.get_product_status.delay(id_product_status)
    return task.get()


@router.get("/add-product-status")
async def add_product_status(name: str) -> int:
    """Add an product status"""
    task = tasks.add_product_status.delay(name)
    return task.get()


@router.put("/update-product-status/{id_product_status}")
async def update_product_status(id_product_status: int, name: str) -> int:
    """Update an product status"""
    task = tasks.update_product_status.delay(id_product_status, name)
    return task.get()


@router.delete("/delete-product-status/{id_product_status}")
async def delete_product_status(id_product_status: int) -> int:
    """Delete an product status"""
    task = tasks.delete_product_status.delay(id_product_status)
    return task.get()


# Location routes
@router.get("/get-locations")
async def get_locations() -> schemas.GetLocationsResponse:
    """Get all locations"""
    task = tasks.get_locations.delay()
    return task.get()


@router.get("/get-location/{location_id}")
async def get_location(location_id: int) -> schemas.LocationBase:
    """Get a location"""
    task = tasks.get_location.delay(location_id)
    return task.get()


@router.get("/add-location")
async def add_location(name: str) -> int:
    """Add a location"""
    task = tasks.add_location.delay(name)
    return task.get()


@router.put("/update-location/{location_id}")
async def update_location(location_id: int, name: str) -> int:
    """Update a location"""
    task = tasks.update_location.delay(location_id, name)
    return task.get()


@router.delete("/delete-location/{location_id}")
async def delete_location(location_id: int) -> int:
    """Delete a location"""
    task = tasks.delete_location.delay(location_id)
    return task.get()


# product routes
@router.get("/")
async def get_products(
        shipping_group_name: str | None = None,
        shipping_label: str | None = None,
        ) -> schemas.GetProductsDetailResponse:
    """Get all products"""
    task = tasks.get_products.delay(
        shipping_group_name=shipping_group_name,
        shipping_label=shipping_label,
    )
    return task.get()


@router.get("/{product_id}")
async def get_product_by_id(product_id: int) -> schemas.ProductDetailResponse:
    """Get an product"""
    task = tasks.get_product.delay(product_id)
    return task.get()


# This method is to perform an add-product but taking the params from the body
@router.post("/")
async def add_product(product: schemas.AddProductInput) -> int:
    """Add an product"""
    task = tasks.add_product_with_ids.delay(
        description=product.description,
        shipping_label=product.shipping_label,
        purchase_price=product.purchase_price,
        product_location_id=product.product_location_id,
        product_status_id=product.product_status_id,
        shipping_group_id=product.shipping_group_id,
    )
    return task.get()


@router.put("/{product_id}")
async def update_product(
    product_id: int,
    description: str | None = None,
    shipping_label: str | None = None,
    purchase_price: float | None = None,
    id_product_status: int | None = None,
    id_location: int | None = None,
    id_shipping_group: int | None = None,
    sale_price: float | None = None,
) -> schemas.UpdateproductResponse:
    """Update an product"""
    task = tasks.update_product.delay(
        product_id=product_id,
        description=description,
        shipping_label=shipping_label,
        purchase_price=purchase_price,
        sale_price=sale_price,
        id_product_status=id_product_status,
        id_location=id_location,
        id_shipping_group=id_shipping_group,
    )
    return task.get()


@router.delete("/{product_id}")
async def delete_product(product_id: int) -> int:
    """Delete an product"""
    task = tasks.delete_product.delay(product_id)
    return task.get()


@router.post("/add-sale-price")
async def add_sale_price(
        shipping_group_name: str,
        shipping_label: str,
        sale_price: float,
) -> int:
    """Add a sale price"""
    task = tasks.add_sale_price.delay(
        shipping_group_name=shipping_group_name,
        shipping_label=shipping_label,
        sale_price=sale_price,
    )
    return task.get()
