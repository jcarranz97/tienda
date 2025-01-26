#!/usr/bin/env python
"""Router for the API for product management."""
from fastapi import APIRouter
from fastapi import Depends
from typing import Annotated
from . import schemas
from . import tasks
from auth.auth import (
    get_current_user,
)
from auth.models import (
    User,
)

router = APIRouter()


@router.get("/get-products-statuses")
async def get_products_statuses(
    current_user: Annotated[User, Depends(get_current_user)],
) -> schemas.GetproductsStatusesResponse:
    """Get all products statuses"""
    task = tasks.get_product_statuses.delay()
    return task.get()


@router.get("/get-product-status/{id_product_status}")
async def get_product_status(
    id_product_status: int,
    current_user: Annotated[User, Depends(get_current_user)],
) -> schemas.ProductStatusBase:
    """Get an product status"""
    task = tasks.get_product_status.delay(id_product_status)
    return task.get()


@router.get("/add-product-status")
async def add_product_status(
    name: str,
    current_user: Annotated[User, Depends(get_current_user)],
) -> int:
    """Add an product status"""
    task = tasks.add_product_status.delay(name)
    return task.get()


@router.put("/update-product-status/{id_product_status}")
async def update_product_status(
    id_product_status: int,
    name: str,
    current_user: Annotated[User, Depends(get_current_user)],
) -> int:
    """Update an product status"""
    task = tasks.update_product_status.delay(id_product_status, name)
    return task.get()


@router.delete("/delete-product-status/{id_product_status}")
async def delete_product_status(
    id_product_status: int,
    current_user: Annotated[User, Depends(get_current_user)],
) -> int:
    """Delete an product status"""
    task = tasks.delete_product_status.delay(id_product_status)
    return task.get()


# Location routes
@router.get("/get-locations")
async def get_locations(
    current_user: Annotated[User, Depends(get_current_user)],
) -> schemas.GetLocationsResponse:
    """Get all locations"""
    task = tasks.get_locations.delay()
    return task.get()


@router.get("/get-location/{location_id}")
async def get_location(
    location_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
) -> schemas.LocationBase:
    """Get a location"""
    task = tasks.get_location.delay(location_id)
    return task.get()


@router.get("/add-location")
async def add_location(
    name: str,
    current_user: Annotated[User, Depends(get_current_user)],
) -> int:
    """Add a location"""
    task = tasks.add_location.delay(name)
    return task.get()


@router.put("/update-location/{location_id}")
async def update_location(
    location_id: int,
    name: str,
    current_user: Annotated[User, Depends(get_current_user)],
) -> int:
    """Update a location"""
    task = tasks.update_location.delay(location_id, name)
    return task.get()


@router.delete("/delete-location/{location_id}")
async def delete_location(
    location_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
) -> int:
    """Delete a location"""
    task = tasks.delete_location.delay(location_id)
    return task.get()


# product routes
@router.get("/")
async def get_products(
        current_user: Annotated[User, Depends(get_current_user)],
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
async def get_product_by_id(
    product_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
) -> schemas.ProductDetailResponse:
    """Get an product"""
    task = tasks.get_product.delay(product_id)
    return task.get()


# This method is to perform an add-product but taking the params from the body
@router.post("/")
async def add_product(
    product: schemas.AddProductInput,
    current_user: Annotated[User, Depends(get_current_user)],
) -> int:
    """Add an product"""
    task = tasks.add_product_with_ids.delay(
        description=product.description,
        shipping_label=product.shipping_label,
        purchase_price=product.purchase_price,
        product_location_id=product.product_location_id,
        shipping_group_id=product.shipping_group_id,
        length=product.length,
        width=product.width,
        height=product.height,
    )
    return task.get()


@router.put("/{product_id}")
async def update_product(
    product_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
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


@router.put("/{product_id}/size")
async def update_product_size(
    product_id: int,
    product_size: schemas.AddProductSizeInput,
    current_user: Annotated[User, Depends(get_current_user)],
) -> schemas.ProductDetailResponse:
    """Update an product size"""
    task = tasks.update_product_size.delay(
        product_id=product_id,
        length=product_size.length,
        width=product_size.width,
        height=product_size.height,
    )
    return task.get()


@router.put("/{product_id}/material")
async def update_product_material(
    product_id: int,
    material: schemas.UpdateProductMaterialInput,
    current_user: Annotated[User, Depends(get_current_user)],
) -> schemas.ProductDetailResponse:
    """Update an product material"""
    task = tasks.update_product_material.delay(
        product_id=product_id,
        material=material.material,
    )
    return task.get()


@router.delete("/{product_id}")
async def delete_product(
    product_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
) -> int:
    """Delete an product"""
    task = tasks.delete_product.delay(product_id)
    return task.get()


@router.post("/{product_id}/add-sale-price")
async def add_sale_price_with_id_w(
        product_id: int,
        body: schemas.AddSalePriceInput,
        current_user: Annotated[User, Depends(get_current_user)],
        ) -> schemas.ProductDetailResponse:
    """Add a sale price"""
    task = tasks.add_sale_price_with_id_2.delay(
        id_product=product_id,
        sale_price=body.sale_price,
    )
    return task.get()
