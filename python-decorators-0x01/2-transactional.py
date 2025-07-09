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

with_db_connection = __import__('1-with_db_connection.with_db_connection')


def transactional(function: Any):
    pass

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
