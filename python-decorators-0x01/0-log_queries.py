"""
#! 0. Logging database Queries

#? Objective: create a decorator that logs database queries executed by any function

Instructions:

    Complete the code below by writing a decorator log_queries that logs the SQL query before executing it.

    Prototype: def log_queries()
"""

from typing import Any
from psycopg2 import connect, DatabaseError
from psycopg2.extensions import connection
from dotenv import load_dotenv
from datetime import datetime
import os
import logging

load_dotenv()  # loading env variables from .env file


def connect_db():
    """
    Function for connecting to a Database

    Asynchronously establishes a connection to a database using credentials and configuration
    retrieved from environment variables. If the connection is successful, returns the connection
    object; otherwise, prints the exception encountered.
    Returns:
        connection: A database connection object if successful.
    Raises:
        Exception: If the connection to the database fails.
    """

    USER = os.getenv("USER")
    PASSWORD = os.getenv("PASSWORD")
    DATABASE = os.getenv("DATABASE")
    PORT = os.getenv("PORT")

    try:
        conn: connection = connect(
            dbname=DATABASE, user=USER, password=PASSWORD, port=PORT)
        return conn
    except (DatabaseError) as e:
        print(f'Failed to connect to the database: {e}')
        raise e


def log_queries(function):  # type: ignore

    def wrapper(*args: Any, **kwargs: Any) -> None:
        logger = logging.getLogger(__name__)

        # TODO: log query before executing it
        logger.info(f'QUERY: {args[0]} - {datetime.now()}')
        print(f'QUERY: {args[0]} - {datetime.now()}')

        function(*args, **kwargs)

    return wrapper


@log_queries
def fetch_all_users(query: str):
    try:
        with connect_db() as conn:
            with conn.cursor() as cursor:
                result = cursor.execute(query)  # type: ignore
                rows = cursor.fetchall()

                if not rows:
                    return

                for r in rows:
                    print(r)
    except DatabaseError as db_e:
        print(f'Error: {db_e}')
        raise db_e


def main():
    query = "SELECT * FROM user_data;"
    fetch_all_users(query)


if __name__ == "__main__":
    main()
