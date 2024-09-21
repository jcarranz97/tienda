#!/usr/bin/env python
"""Main module for the FastAPI application."""
import asyncio
from typing import Annotated
from fastapi import FastAPI
from fastapi import WebSocket
from fastapi import Depends
from fastapi.responses import JSONResponse
from celery.result import AsyncResult
from celery_worker import celery_app
from sellers.router import router as sellers_router
from shippers.router import router as shippers_router
from group2.router import router as group2_router
from auth import get_current_username


app = FastAPI()
app.include_router(sellers_router, prefix="/sellers", tags=["sellers"])
app.include_router(shippers_router, prefix="/shippers", tags=["shippers"])
app.include_router(group2_router, prefix="/group2")


# Include exception handlers
# pylint: disable=unused-argument
@app.exception_handler(ValueError)
async def value_error_exception_handler(request, exc):
    """Exception handler for ValueError."""
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)},
    )


@app.get("/")
def read_root():
    """Hello World endpoint."""
    return {"Hello": "World"}


@app.websocket("/ws/task/{task_id}")
async def websocket_endpoint(websocket: WebSocket, task_id: str):
    """Websocket endpoint to get the task result."""
    await websocket.accept()

    # Get the task result asynchronously
    result = AsyncResult(task_id, app=celery_app)

    while not result.ready():
        await websocket.send_text("Processing...")
        await asyncio.sleep(1)

    # If result is successful, send the state and result
    if result.successful():
        await websocket.send_text(f"Task {task_id} succeeded: {result.result}")
    else:
        await websocket.send_text(f"Task {task_id} failed: {result.result}")


@app.get("/users/me")
def read_current_user(username: Annotated[str, Depends(get_current_username)]):
    """Get the current user.

    This method is mainly for testing the dependency injection. In this case
    the basic auth is used to get the username.
    """
    return {"username": username}
