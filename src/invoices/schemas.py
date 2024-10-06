#!/usr/bin/python3
"""Seller schemas"""
from datetime import date
from pydantic import BaseModel


class InvoiceDetails(BaseModel):
    """Invoice details schema"""
    id: int
    notes: str
    seller_name: str
    total_amount: float
    num_products: int
    num_payments: int
    total_paid: float


class GetInvoicesDetailsResponse(BaseModel):
    """Get sellers response schema"""
    invoices: list[InvoiceDetails]
    num_invoices: int


class CreateInvoiceRequest(BaseModel):
    """Create invoice request schema"""
    id_seller: int
    notes: str
    products: list[int] | None
    payment: float | None


class InvoicePaymentDetails(BaseModel):
    """Invoice payment details schema"""
    id: int
    amount: float
    payment_date: date
    payment_comment: str | None


class GetInvoicePaymentsResponse(BaseModel):
    """Get invoice payments response schema"""
    payments: list[InvoicePaymentDetails]
    num_payments: int


class AddInvoicePaymentRequest(BaseModel):
    """Add invoice payment request schema"""
    amount: float
    payment_date: date
    payment_comment: str | None


class InvoiceProductDetails(BaseModel):
    """Invoice product details schema"""
    id: int
    shipping_label: str
    description: str
    sale_price: float


class GetInvoiceProductsResponse(BaseModel):
    """Get invoice products response schema"""
    products: list[InvoiceProductDetails]
    num_products: int
