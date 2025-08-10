"""
#! 2. Transaction Management Decorator

#? Objective: create a decorator that manages database transactions by automatically committing or rolling back changes

Instructions:

    Complete the script below by writing a decorator transactional(func) that ensures a function running a database operation is wrapped inside a transaction.If the function raises an error, rollback; otherwise commit the transaction.

    Copy the with_db_connection created in the previous task into the script
"""

from typing import Any
from psycopg2 import connect, DatabaseError  # type:ignore
from psycopg2.extensions import connection
from dotenv import load_dotenv
import os  # type:ignore

load_dotenv()


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


def transactional(function: Any):
    def wrapper(*args: Any, **kwargs: Any):
        with connect_db() as conn:
            function(*args, conn)

    return wrapper


@transactional
def update_user_email(*args: Any):
    user_id: str = args[0]
    email: str = args[1]
    conn: connection = args[2]

    with conn.cursor() as cursor:
        try:
            query = "UPDATE user_data SET email = %s WHERE user_id = %s"
            cursor.execute(query, (email, user_id))
            conn.commit()

        except DatabaseError as db_err:
            print(f'Exception: {db_err}')
            conn.rollback()


def main():
    update_user_email("bcfb0c90-3d44-4806-8cb4-5763ed77f796",
                      "updatedemail@mail.com")


if __name__ == '__main__':
    main()
