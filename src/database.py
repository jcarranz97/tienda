#!\usr\bin\env python3
"""Module to handle database operations."""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

load_dotenv()


def _get_db_url():
    """Return the database URL."""
    db_host = os.getenv('DB_HOST')
    db_user = os.getenv('DB_USER')
    db_port = os.getenv('DB_PORT')
    db_pass = os.getenv('DB_PASS')
    db_name = os.getenv('DB_NAME')
    return f"mysql+mysqlconnector://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"


engine = create_engine(_get_db_url(), pool_pre_ping=True, pool_recycle=3600)
Session = scoped_session(sessionmaker(bind=engine))
