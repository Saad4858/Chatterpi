import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database, drop_database

def get_connection_string() -> str:
    load_dotenv()

    connection_string = f"{os.getenv('DB_TYPE')}://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

    return connection_string

def validate_db():
    connection_string = get_connection_string()
    if not database_exists(connection_string):
        create_database(connection_string)
        print(f"Database created: {connection_string}")
    else:
        print(f"Database already exists: {connection_string}")

def get_engine():
    load_dotenv()

    connection_string = f"{os.getenv('DB_TYPE')}://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

    engine = create_engine(connection_string)

    return engine

def wipe_database():
    load_dotenv()

    connection_string = f"{os.getenv('DB_TYPE')}://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

    if database_exists(connection_string):
        drop_database(connection_string)
        print(f"Database destroyed: {connection_string}")
    else:
        print(f"Database doesn't exist: {connection_string}")