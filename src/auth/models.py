#!/usr/bin/env python3
"""Module that defines the authentication for the API."""
from pydantic import BaseModel


class Token(BaseModel):
    """Model for a token."""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Model for token data."""

    username: str | None = None


class User(BaseModel):
    """Model for a user."""

    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    """Model for a user in the database."""
    hashed_password: str
