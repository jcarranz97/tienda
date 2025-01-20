#!/usr/bin/env python
"""Celery worker module."""
import os
from celery import Celery

CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")
print("CELERY_BROKER_URL - ", CELERY_BROKER_URL)
if not CELERY_BROKER_URL:
    CELERY_BROKER_URL = "redis://redis:6379/0"
    print("CELERY_BROKER_URL (local) - ", CELERY_BROKER_URL)

celery_app = Celery(
    "tasks",
    broker=CELERY_BROKER_URL,
    backend=CELERY_BROKER_URL,
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
