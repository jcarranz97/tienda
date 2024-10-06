#!/usr/bin/env python
"""FastAPI router related to group1."""
from fastapi import APIRouter
from . import tasks
from . import schemas

router = APIRouter()


@router.get("/")
async def get_invoices() -> schemas.GetInvoicesDetailsResponse:
    """Get invoices"""
    task = tasks.get_invoices.delay()
    return task.get()


@router.get("/{invoice_id}")
async def get_invoice(invoice_id: int) -> schemas.InvoiceDetails:
    """Get invoice"""
    task = tasks.get_invoice.delay(invoice_id)
    return task.get()


@router.post("/")
async def create_invoice(request: schemas.CreateInvoiceRequest) -> int:
    """Create invoice

    This endpoint creates an invoice and returns the invoice id. If the request
    contains a list of products, it adds them to the invoice. If the request
    contains a payment, it adds it to the invoice.
    """
    task = tasks.create_invoice.delay(
        request.id_seller,
        request.notes,
    )
    invoice_id = task.get()
    print("Invoice ID:", invoice_id)
    # Add products to the invoice if they are provided
    if request.products:
        for product_id in request.products:
            task = tasks.add_invoice_product.delay(invoice_id, product_id)
    # Wait for the last task to finish
    task.get()

    # Add payment to the invoice if it is provided
    if request.payment:
        task = tasks.add_invoice_payment.delay(invoice_id, request.payment)
    # Wait for the last task to finish
    task.get()

    return invoice_id


@router.get("/{invoice_id}/payments")
async def get_invoice_payments(
        invoice_id: int
) -> schemas.GetInvoicePaymentsResponse:
    """Get invoice payments"""
    task = tasks.get_invoice_payments.delay(invoice_id)
    return task.get()


@router.post("/{invoice_id}/payments")
async def add_invoice_payment(
        invoice_id: int,
        request: schemas.AddInvoicePaymentRequest
        ) -> schemas.InvoicePaymentDetails:
    """Add invoice payment"""
    task = tasks.add_invoice_payment.delay(
        id_invoice=invoice_id,
        amount=request.amount,
        payment_date=request.payment_date,
        payment_comment=request.payment_comment,
    )
    return task.get()


@router.get("/{invoice_id}/products")
async def get_invoice_products(
        invoice_id: int
) -> schemas.GetInvoiceProductsResponse:
    """Get invoice products"""
    task = tasks.get_invoice_products.delay(invoice_id)
    return task.get()
