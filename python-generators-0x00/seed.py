"""
#! Objective: create a generator that streams rows from an SQL database one by one

#? Setup a SQL database with the table user_data:
create table user_data(
    user_id UUID DEFAULT gen_random_uuid() PRIMARY KEY NOT NULL,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    age DECIMAL NOT NULL
);


#? Populate the database with sample data from [user_data.csv]
insert into user_data (name, email, age) values ('Johnnie Mayer','Ross.Reynolds21@hotmail.com',35);

#? Functions
#* def connect_db() -> connects to the database
#* def create_db(connection) -> creates the database [ALX_prodev] if it does not exist
#* def connect_to_prodev(connection) -> connects the [ALX_prodev] database in SQL
#* def create_table(connection) -> creates a table `user_data` if does not exist with required fields 
#* def insert_data(connection, data) -> inserts data in the database if it doesn't exist
"""

from typing import Any
import asyncio
from psycopg2 import connect
from psycopg2.extensions import connection
from dotenv import load_dotenv
import os

load_dotenv()


async def connect_db():
    """
    ! Coroutine for connecting to a Database
    """

    USER = os.getenv("USER")
    PASSWORD = os.getenv("PASSWORD")
    DATABASE = os.getenv("DATABASE")
    PORT = os.getenv("PORT")

    try:
        conn: connection = connect(
            dbname=DATABASE, user=USER, password=PASSWORD, port=PORT
        )

        print("Connected to the DB...")

        return conn

    except Exception as e:
        print(f'Exception:', e)


def create_db(conn: connection):
    pass


def connect_to_prodev(conn: connection):
    pass


def create_table(conn: connection):
    pass


def insert_data(conn: connection, data: Any):
    pass


async def main():
    await connect_db()


if __name__ == "__main__":
    asyncio.run(main())
