"""
Create a SQLAlchemy engine for PostgreSQL from environment variables.
"""
import os

from dotenv import load_dotenv
from sqlalchemy import Engine, create_engine

# Read .env in the current folder into environment variables.
# Inside Docker the variables are by Compose instead.
load_dotenv()

def get_engine() -> Engine:
    url = (
        f"postgresql+psycopg://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}"
        f"@{os.environ['POSTGRES_HOST']}:{os.environ['POSTGRES_PORT']}/{os.environ['POSTGRES_DB']}"
    )
    return create_engine(url)
