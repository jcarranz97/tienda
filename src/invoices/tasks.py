#!/usr/bin/env python
"""Celery tasks related to sellers."""
from celery import shared_task
from database import Session
from . import models
from . import schemas
from . import queries


@shared_task
def get_invoices():
    """Get invoices task"""
    # Create a session
    with Session() as session:
        # Get the invoices
        query = queries.get_invoices_query(session)

        # Get invoices
        invoices = [
            schemas.InvoiceDetails(
                id=db_invoice.id_invoice,
                notes=db_invoice.notes,
                seller_name=db_invoice.seller_name,
                total_amount=db_invoice.total_amount,
                num_products=db_invoice.num_products,
                num_payments=db_invoice.num_payments,
                total_paid=db_invoice.total_paid,
            ).dict()
            for db_invoice in query.all()
        ]
        return schemas.GetInvoicesDetailsResponse(
            invoices=invoices,
            num_invoices=len(invoices),
        ).dict()


@shared_task
def get_invoice(
        invoice_id: int,
):
    """Get invoice task"""
    # Create a session
    with Session() as session:
        # Get the invoice
        db_invoice = queries.get_invoices_query(session, invoice_id).first()
        # Return the invoice
        return schemas.InvoiceDetails(
            id=db_invoice.id_invoice,
            notes=db_invoice.notes,
            seller_name=db_invoice.seller_name,
            total_amount=db_invoice.total_amount,
            num_products=db_invoice.num_products,
            num_payments=db_invoice.num_payments,
            total_paid=db_invoice.total_paid,
        ).dict()


@shared_task
def create_invoice(
        id_seller: int,
        notes: str,
):
    """Create invoice task"""
    # Create a session
    with Session() as session:
        # Create the invoice
        invoice = models.Invoice(
            id_seller=id_seller,
            notes=notes,
        )
        session.add(invoice)
        session.commit()
        # Return the invoice
        return invoice.id_invoice


@shared_task
def add_invoice_product(
        id_invoice: int,
        id_product: int,
):
    """Add product to invoice task"""
    # Create a session
    with Session() as session:
        # Create the invoice detail
        invoice_detail = models.InvoiceDetail(
            id_invoice=id_invoice,
            id_product=id_product,
        )
        session.add(invoice_detail)
        session.commit()
        # Return the invoice detail
        return invoice_detail.id_invoice_detail


@shared_task
def add_invoice_payment(
        id_invoice: int,
        amount: float,
):
    """Add payment to invoice task"""
    # Create a session
    with Session() as session:
        # Create the invoice payment
        invoice_payment = models.InvoicePayment(
            id_invoice=id_invoice,
            amount=amount,
        )
        session.add(invoice_payment)
        session.commit()
        # Return the invoice payment
        return invoice_payment.id_invoice_payment


@shared_task
def get_invoice_payments(
        invoice_id: int,
):
    """Get invoice payments task"""
    # Create a session
    with Session() as session:
        # Get the invoice payments
        query = queries.get_invoices_payments_query(
            session, invoice_id
        )

        # Get invoice payments
        payments = [
            schemas.InvoicePaymentDetails(
                id=db_payment.id_invoice_payment,
                amount=db_payment.amount,
                payment_date=db_payment.created_at,
            ).dict()
            for db_payment in query.all()
        ]
        return schemas.GetInvoicePaymentsResponse(
            payments=payments,
            num_payments=len(payments),
        ).dict()
