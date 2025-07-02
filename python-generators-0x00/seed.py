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
#* def connect_to_prodev(connection) -> connects the [ALX_prodev] database
#* def create_table(connection) -> creates a table `user_data` if does not exist with required fields 
#* def insert_data(connection, data) -> inserts data in the database if it doesn't exist
"""

import asyncio
from psycopg2 import connect, DatabaseError
from psycopg2.extensions import connection
from dotenv import load_dotenv
import os

load_dotenv()  # loading env variables from .env file


class User:
    def __init__(self, name: str, email: str, age: int) -> None:
        self.name = name
        self.email = email
        self.age = age

    def __str__(self) -> str:
        return f'[name: {self.name}, email: {self.email}, age: {self.age}]'


def connect_db():
    """
    ! Coroutine for connecting to a Database

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


def create_db(conn: connection):
    """
    Creates the 'ALX_prodev' database if it does not already exist.
    Args:
        conn (connection): A database connection object used to execute SQL commands.
    Raises:
        Exception: If there is an error during database creation.
    Returns:
        None
    creates the database [ALX_prodev] if it does not exist
    """
    try:
        conn.autocommit = True

        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT 1 FROM pg_database WHERE datname = 'alx_prodev';")

            exists = cursor.fetchone()

            if not exists:
                cursor.execute("CREATE DATABASE ALX_prodev;")
                print("Database 'ALX_prodev' created.")
            else:
                print("Database 'ALX_prodev' already exists.")

    except Exception as e:
        print(f"Error creating database: {e}")
        raise
    finally:
        conn.autocommit = False


def insert_data(conn: connection, data: User):
    """
    ! Inserts a new user record into the user_data table and returns the generated user_id.
    Args:
        conn (connection): Database connection object.
        data (User): User object containing name, email, and age.
    Returns:
        str: The user_id of the newly inserted user.
    """
    user_id = ""
    command = """
    INSERT INTO user_data (name, email, age) VALUES (%s, %s, %s)
        RETURNING user_id;
    """

    with conn.cursor() as cursor:
        cursor.execute(command, (data.name, data.email, data.age))

        rows = cursor.fetchone()

        if rows:
            user_id = rows[0]
            print(f'User created:', user_id)

        conn.commit()

        return user_id
    try:
        pass
    except DatabaseError as de:
        print(f'Error: {de}')
    finally:
        conn.close()


def connect_to_prodev(conn: connection):
    """
    connects the [alx_prodev] database
    """
    try:
        conn.autocommit = True

        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT 1 FROM pg_database WHERE datname = 'alx_prodev';")
            exists = cursor.fetchone()

            if exists:
                print("Connected to 'alx_prodev' database.")
            else:
                print("'alx_prodev' database does not exist.")
    except Exception as e:
        print(f"Error connecting to 'alx_prodev': {e}")
        raise
    finally:
        conn.autocommit = False


def create_table(conn: connection):
    try:
        command = """
        CREATE TABLE user_data(
            user_id UUID DEFAULT gen_random_uuid() PRIMARY KEY NOT NULL,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL NOT NULL
        )
        """
        with conn.cursor() as cursor:
            cursor.execute(command)

    except Exception as e:
        print(f'Error: {e}')


def main():
    conn: connection = connect_db()

    create_db(conn)
    connect_to_prodev(conn)
    insert_data(conn, User('Hero Scxxt', 'hero@mail.com', 25))

    with conn.cursor() as cursor:
        command = """SELECT * FROM user_data;"""
        cursor.execute(command)

        rows = cursor.fetchall()

        print("Num rows:", cursor.rowcount)

        for r in rows:
            print(r)


if __name__ == "__main__":
    main()
