#!/usr/bin/env python
"""This module defines common queries for invoice management."""
from sqlalchemy import func
from sqlalchemy import case
from products.models import Product
from sellers.models import Seller
from . import models


def get_invoices_query(session, invoice_id=None):
    """Get invoice query."""
    # Define aliases for clarity (optional)
    # This query fetches the required fields, including the "total_amount"
    # number of products, number of payments, and the total paid amount

    # Subquery to get the total payments for each invoice
    payment_subquery = (
        session.query(
            models.InvoicePayment.id_invoice,
            func.count(models.InvoicePayment.id_invoice_payment).label('num_payments'),  # pylint: disable=not-callable,line-too-long # noqa E501
            func.coalesce(func.sum(models.InvoicePayment.amount), 0).label('total_paid')
        )
        .group_by(models.InvoicePayment.id_invoice)
        .subquery()
    )

    # Calculate the total amount (sum of product sale prices)
    total_amount = func.coalesce(func.sum(Product.sale_price), 0).label('total_amount')

    # Calculate the remaining balance
    total_paid = func.coalesce(payment_subquery.c.total_paid, 0).label('total_paid')
    remaining_balance = (total_amount - total_paid).label('remaining_balance')

    # Add the invoice status: "pending" if total_paid < total_amount, otherwise "paid"
    invoice_status = case(
        (total_paid < total_amount, 'pending'),    # When total_paid is less than total_amount
        (total_paid > total_amount, 'overpaid'),   # When total_paid is greater than total_amount
        else_='paid'
    ).label('invoice_status')

    # Main query fetching invoice details
    query = (
        session.query(
            models.Invoice.id_invoice,
            models.Invoice.notes,
            Seller.seller_name,
            total_amount,
            func.count(Product.id_product).label('num_products'),  # pylint: disable=not-callable
            func.coalesce(payment_subquery.c.num_payments, 0).label('num_payments'),
            total_paid,
            # Calculate the remaining amount by subtracting the total paid from the total amount
            remaining_balance,
            invoice_status,
        )
        .join(models.InvoiceDetail, models.Invoice.id_invoice == models.InvoiceDetail.id_invoice)
        .join(Product, models.InvoiceDetail.id_product == Product.id_product)
        .join(Seller, models.Invoice.id_seller == Seller.id_seller)
        .outerjoin(payment_subquery, models.Invoice.id_invoice == payment_subquery.c.id_invoice)
        .group_by(
            models.Invoice.id_invoice,
            Seller.seller_name,
            models.Invoice.notes
        )
    )

    if invoice_id:
        query = query.filter(models.Invoice.id_invoice == invoice_id)

    return query


def get_invoices_payments_query(
        session,
        invoice_id=None,
):
    """Get invoice payments query"""
    # This query fetches the payments related to the invoice and returns
    # the id, amount and the date of the payment
    query = (
        session.query(
            models.InvoicePayment.id_invoice_payment,
            models.InvoicePayment.amount,
            models.InvoicePayment.payment_date,
            models.InvoicePayment.payment_comment,
        )
    )

    if invoice_id:
        query = query.filter(models.InvoicePayment.id_invoice == invoice_id)

    return query


def get_invoices_products_query(
        session,
        invoice_id=None,
):
    """Get invoice products query"""
    # This query fetches the products related to the invoice and returns
    # the id, name, and sale price of the product
    query = (
        session.query(
            Product.id_product,
            Product.description,
            Product.shipping_label,
            Product.sale_price,
        )
        .join(models.InvoiceDetail, Product.id_product == models.InvoiceDetail.id_product)
    )

    if invoice_id:
        query = query.filter(models.InvoiceDetail.id_invoice == invoice_id)

    return query
