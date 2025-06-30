"""
#! Objective: create a generator that streams rows from an SQL database one by one

#? Setup a SQL database with the table user_data:
create table user_data(
    user_id UUID PRIMARY KEY NOT NULL,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    age DECIMAL NOT NULL
);

#? Populate the database with sample data from [user_data.csv]

#* def connect_db() -> connects to the database
#* def create_db(connection) -> creates the database [ALX_prodev] if it does not exist
#* def connect_to_prodev(connection) -> connects the [ALX_prodev] database in SQL
#* def create_table(connection) -> creates a table `user_data` if does not exist with required fields 
#* def insert_data(connection, data) -> inserts data in the database if it doesn't exist
"""

from typing import Any


def connect_db():
    pass


def create_db(connection: Any):
    pass


def connect_to_prodev(connection: Any):
    pass


def create_table(connection: Any):
    pass


def insert_data(connection: Any, data: Any):
    pass


def main():
    print("hello test")


if __name__ == "__main__":
    main()
