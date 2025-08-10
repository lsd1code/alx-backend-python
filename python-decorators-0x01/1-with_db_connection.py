"""
#! 1. Handle Database Connections with a Decorator

#? Objective: create a decorator that automatically handles opening and closing database connections

Instructions:

    Complete the script below by Implementing a decorator with_db_connection that opens a database connection, passes it to the function and closes it afterword
"""

from typing import Any
from psycopg2 import connect, DatabaseError  # type:ignore
from psycopg2.extensions import connection
from dotenv import load_dotenv
import os  # type:ignore

load_dotenv()


def with_db_connection(function):  # type: ignore
    def connect_db():
        try:
            USER = os.getenv("USER")
            PASSWORD = os.getenv("PASSWORD")
            DATABASE = os.getenv("DATABASE")
            PORT = os.getenv("PORT")

            conn: connection = connect(
                dbname=DATABASE, user=USER, password=PASSWORD, port=PORT)
            return conn
        except (DatabaseError) as e:
            print(f'Failed to connect to the database: {e}')
            raise e

    def wrapper(*args: Any, **kwargs: Any):
        with connect_db() as conn:
            function(*args, conn)

    return wrapper


@with_db_connection
def get_user_by_id(*args: Any):
    conn: connection = args[1]
    user_id: str = args[0]

    with conn.cursor() as cursor:
        cursor.execute(
            'SELECT * FROM user_data WHERE user_id = %s;', (user_id,))
        rows = cursor.fetchall()

        if rows:
            for r in rows:
                print(r)


def main():
    get_user_by_id("bcfb0c90-3d44-4806-8cb4-5763ed77f796")


if __name__ == '__main__':
    main()
