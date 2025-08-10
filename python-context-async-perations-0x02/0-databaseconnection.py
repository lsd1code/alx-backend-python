"""
#! Custom class based context manager for Database connection

#? Objective: create a class based context manager to handle opening and closing database connections automatically

Instructions:

    Write a class custom context manager DatabaseConnection using the __enter__ and the __exit__ methods

    Use the context manager with the with statement to be able to perform the query SELECT * FROM users. Print the results from the query.
"""

# from typing import Any
# from psycopg2.extensions import connection
from psycopg2 import connect, DatabaseError
from dotenv import load_dotenv
import os

load_dotenv()


class DatabaseConnection:
    def __init__(self) -> None:
        self.conn = None  # type: ignore

    def __enter__(self):
        try:
            USER = os.getenv("USER")
            PASSWORD = os.getenv("PASSWORD")
            DATABASE = os.getenv("DATABASE")
            PORT = os.getenv("PORT")

            self.conn = connect(dbname=DATABASE, user=USER,
                                password=PASSWORD, port=PORT)
            return self.conn
        except DatabaseError as db_e:
            print(f'Could not connect to the Database. Please try again!')
            raise db_e

    def __exit__(self, exc_type, exc_value, exc_tb):  # type:ignore
        if self.conn:
            self.conn.close()


def main():
    with DatabaseConnection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM user_data;")
            rows = cursor.fetchall()

            if rows:
                for r in rows:
                    print(r)

        print(conn)


if __name__ == "__main__":
    main()
