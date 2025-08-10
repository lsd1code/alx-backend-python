"""
#! Memory-Efficient Aggregation with Generators

#? Objective: to use a generator to compute a memory-efficient aggregate function i.e average age for a large dataset

Instruction:

    Implement a generator stream_user_ages() that yields user ages one by one.

    Use the generator in a different function to calculate the average age without loading the entire dataset into memory

    Your script should print Average age of users: average age

    You must use no more than two loops in your script

    You are not allowed to use the SQL AVERAGE
"""

from typing import Any, Generator
from seed import connect_db


def stream_user_ages():
    """
    Generator function that streams user ages from the 'user_data' database table.
    Yields:
        int: The age of each user retrieved from the database.
    Raises:
        Any exceptions raised by the database connection or query execution.
    Usage:
        for age in stream_user_ages():
            print(age)
    """

    command = """SELECT age FROM user_data;"""

    with connect_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(command)
            rows = cursor.fetchall()

            if rows:
                for r in rows:
                    yield int(r[0])


def calc_user_avg_age(gen: Generator[int, Any, None]):
    """
    Calculates the average age from a generator of user ages.
    Args:
        gen (Generator[int, Any, None]): A generator that yields user ages as integers.
    Returns:
        float: The average age of users. Returns 0 if the generator yields no ages.
    """

    combined_age = 0
    number_users = 0

    for user_age in gen:
        combined_age += user_age
        number_users += 1

    return round(combined_age / number_users) if number_users > 0 else 0


def main():
    avg_age = calc_user_avg_age(stream_user_ages())
    print(f'Average age of users: {avg_age}')


if __name__ == "__main__":
    main()
