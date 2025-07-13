"""
#! Reusable Query Context Manager

#? Objective: create a reusable context manager that takes a query as input and executes it, managing both connection and the query execution

Instructions:

    Implement a class based custom context manager ExecuteQuery that takes the query: ”SELECT * FROM users WHERE age > ?” and the parameter 25 and returns the result of the query

    Ensure to use the__enter__() and the __exit__() methods
"""

from psycopg2 import connect, DatabaseError
from dotenv import load_dotenv
import os

load_dotenv()


class ExecuteQuery:
    def __init__(self, query: str, param: int) -> None:
        self.query = query
        self.param = param
        self.conn = None

    def __enter__(self):
        try:
            USER = os.getenv("USER")
            PASSWORD = os.getenv("PASSWORD")
            DATABASE = os.getenv("DATABASE")
            PORT = os.getenv("PORT")

            if not self.conn:
                self.conn = connect(dbname=DATABASE, user=USER,
                                    password=PASSWORD, port=PORT)

            with self.conn.cursor() as cursor:
                cursor.execute(self.query, (self.param, ))
                rows = cursor.fetchall()

                if rows:
                    return rows
        except DatabaseError as db_e:
            print(f'Exception: {db_e}')
            raise db_e

    def __exit__(self, exc_type, exec_val, exec_tb):  # type: ignore
        if self.conn:
            self.conn.close()
            print(self.conn)


def main():
    QUERY = "SELECT * FROM user_data WHERE age > 25;"
    PARAM = 25

    with ExecuteQuery(query=QUERY, param=PARAM) as result:
        if result:
            for row in result:
                print(row)


if __name__ == "__main__":
    main()
