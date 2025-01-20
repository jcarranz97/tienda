#!/usr/bin/env python
"""Celery worker module."""
from celery import Celery
import os

CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")
print("CELERY_BROKER_URL - ", CELERY_BROKER_URL)

celery_app = Celery(
    "tasks",
    broker=CELERY_BROKER_URL,
    backend=CELERY_BROKER_URL,
    # backend="redis://redis/0",
    include=[
        "sellers.tasks",
        "shippers.tasks",
        "shipping.tasks",
        "products.tasks",
        "invoices.tasks",
    ],
)

celery_app.conf.task_routes = {
    "sellers.tasks.*": {"queue": "base"},
    "shippers.tasks.*": {"queue": "base"},
    "shipping.tasks.*": {"queue": "base"},
    "products.tasks.*": {"queue": "base"},
    "invoices.tasks.*": {"queue": "base"},
}
