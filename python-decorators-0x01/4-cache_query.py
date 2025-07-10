"""
#! Using decorators to cache Database Queries

#? Objective: create a decorator that caches the results of a database queries in order to avoid redundant calls

Instructions:

    Complete the code below by implementing a decorator cache_query(func) that caches query results based on the SQL query string
"""
from typing import Any
from psycopg2.extensions import connection
from psycopg2 import connect, DatabaseError
from dotenv import load_dotenv
import os

load_dotenv()


query_cache = {}


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


def cache_query(function: Any):
    def wrapper(*args: Any, **kwargs: Any):
        with connect_db() as conn:
            function(*args, conn)

    return wrapper


@cache_query
def fetch_users_with_cache(*args: Any):
    if len(args) < 2:
        return

    query: str = args[0]

    if query_cache.get(query):
        print('Cache HIT')
        return query_cache.get(query)
    
    conn: connection = args[1]

    with conn.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

        if rows:
            query_cache[query] = rows
            return query_cache[query]


def main():
    fetch_users_with_cache("SELECT * FROM user_data;")
    fetch_users_with_cache("SELECT * FROM user_data;")


if __name__ == '__main__':
    main()
