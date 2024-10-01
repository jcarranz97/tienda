#!/usr/bin/python3
"""This module defines the models related to sellers."""
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import Text
from sqlalchemy.orm import relationship
from sqlalchemy import Numeric
from models import Base


class Invoice(Base):
    """Invoice model"""
    __tablename__ = 'invoices'

    id_invoice = Column(Integer, primary_key=True, autoincrement=True)
    id_seller = Column(Integer, ForeignKey('sellers.id_seller'), nullable=False)
    notes = Column(Text, nullable=True)

    # Relationship with InvoiceDetails
    invoice_details = relationship("InvoiceDetail", back_populates="invoice")


class InvoiceDetail(Base):
    """Invoice Detail model"""
    __tablename__ = 'invoice_details'

    id_invoice_detail = Column(Integer, primary_key=True, autoincrement=True)
    id_invoice = Column(Integer, ForeignKey('invoices.id_invoice'), nullable=False)
    id_product = Column(Integer, ForeignKey('products.id_product'), nullable=False)

    # Relationships
    invoice = relationship("Invoice", back_populates="invoice_details")
    product = relationship("Product")  # Assuming you have a Product model defined


class InvoicePayment(Base):
    """Invoice Payment model"""
    __tablename__ = 'invoice_payments'

    id_invoice_payment = Column(Integer, primary_key=True, autoincrement=True)
    id_invoice = Column(Integer, ForeignKey('invoices.id_invoice'), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)

    # Relationship
    invoice = relationship("Invoice")
