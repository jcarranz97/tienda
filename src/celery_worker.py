#!/usr/bin/env python
"""Celery worker module."""
from celery import Celery

celery_app = Celery(
    "tasks",
    broker="redis://redis/0",
    backend="redis://redis/0",
    include=[
        "sellers.tasks",
        "shippers.tasks",
        "shipping.tasks",
        "articles.tasks",
    ],
)

celery_app.conf.task_routes = {
    "sellers.tasks.*": {"queue": "base"},
    "shippers.tasks.*": {"queue": "base"},
    "shipping.tasks.*": {"queue": "base"},
    "articles.tasks.*": {"queue": "base"},
}
