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
async def get_product_status(id_product_status: int) -> schemas.productStatusBase:
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
@router.get("/get-products")
async def get_products(
        shipping_group_name: str | None = None,
        ) -> schemas.GetproductsDetailResponse:
    """Get all products"""
    task = tasks.get_products.delay(
        shipping_group_name=shipping_group_name,
    )
    return task.get()


@router.get("/get-product/{product_id}")
async def get_product(product_id: int) -> schemas.productDetailResponse:
    """Get an product"""
    task = tasks.get_product.delay(product_id)
    return task.get()


@router.get("/get-product-by-shipping-group-and-label")
async def get_product_by_shipping_group_and_label(
    shipping_group_name: str,
    shipping_label: str,
) -> schemas.productDetailResponse:
    """Get an product by shipping group and label"""
    task = tasks.get_product_by_shipping_group_and_label.delay(
        shipping_group_name=shipping_group_name,
        shipping_label=shipping_label,
    )
    return task.get()


@router.get("/add-product")
async def add_product(
    description: str,
    shipping_label: str,
    purchase_price: float,
    product_location: str,
    product_status: str,
    shipping_group_name: str | None = None,
) -> int:
    """Add an product"""
    task = tasks.add_product.delay(
        description,
        shipping_label,
        purchase_price,
        product_location=product_location,
        product_status=product_status,
        shipping_group_name=shipping_group_name,
    )
    return task.get()


@router.put("/update-product/{product_id}")
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


@router.put("/update-product-by-shipping-group-and-label")
async def update_product_by_shipping_group_and_label(
    shipping_group_name: str,
    shipping_label: str,
    description: str | None = None,
    purchase_price: float | None = None,
    sale_price: float | None = None,
    location: str | None = None,
    status: str | None = None,
) -> schemas.UpdateproductResponse:
    """Update an product by shipping group and label"""
    task = tasks.update_product_by_shipping_group_and_label.delay(
        shipping_group_name=shipping_group_name,
        shipping_label=shipping_label,
        description=description,
        purchase_price=purchase_price,
        sale_price=sale_price,
        location=location,
        status=status,
    )
    return task.get()


@router.delete("/delete-product/{product_id}")
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
