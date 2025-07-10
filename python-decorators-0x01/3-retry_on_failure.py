"""
#! 3. Using Decorators to retry database queries

#? Objective: create a decorator that retries database operations if they fail due to transient errors

Instructions:

    Complete the script below by implementing a retry_on_failure(retries=3, delay=2) decorator that retries the function for a certain number of times if it raises an exception
"""

import time
from typing import Any
from psycopg2.extensions import connection
from psycopg2 import connect, DatabaseError
from dotenv import load_dotenv
import os

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


def retry_on_failure(retries: int, delay: int):
    def retry(function: Any):
        def wrapper(*args: Any, **kwargs: Any):
            for attempt in range(retries + 1):
                try:
                    with connect_db() as conn:
                        return function(conn, *args)
                    
                except DatabaseError as db_err:
                    if attempt < retries:
                        print(f"Attempt {(attempt + 1)} failed. Retrying in {delay} seconds...")
                        time.sleep(delay)
                    else:
                        print("All retry attempts failed.")
                        raise db_err
        return wrapper
    return retry


@retry_on_failure(retries=3, delay=2)
def fetch_users_with_retry(*args: Any):
    conn: connection = args[0]

    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM user_data;")
        rows = cursor.fetchall()

        if rows:
            for r in rows:
                print(r)


def main():
    fetch_users_with_retry()


if __name__ == '__main__':
    main()
