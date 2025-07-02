"""
#! Generator that streams rows from an SQL database

#? Objective: create a generator that streams rows from an SQL database one by one.

#? Write a function that uses a generator to fetch rows one by one from the user_data table. You must use the Yield python generator 
"""

from seed import connect_db


def stream_users():
    """
    Generator function that streams user data from the 'user_data' table in the database.
    Establishes a connection to the database, executes a SQL query to retrieve all records from the 'user_data' table,
    and yields each row one at a time. This allows for efficient processing of large datasets without loading all records
    into memory at once.
    Yields:
        tuple: A row from the 'user_data' table.
    Raises:
        Any exceptions raised by the database connection or query execution.
    """

    try:
        with connect_db() as conn:
            with conn.cursor() as cursor:
                command: str = """SELECT * FROM user_data;"""
                cursor.execute(command)
                rows = cursor.fetchall()

                if rows:
                    for row in rows:
                        yield row

    except Exception as e:
        print(f'Error: {e}')
        raise e


def main():
    for data in stream_users():
        print(data)


if __name__ == "__main__":
    main()
