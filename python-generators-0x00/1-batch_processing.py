"""
#! Batch processing Large Data

#? Objective: Create a generator to fetch and process data in batches from the users database

Instructions:
    Write a function stream_users_in_batches(batch_size) that fetches rows in batches

    Write a function batch_processing() that processes each batch to filter users over the age of25`

    You must use no more than 3 loops in your code. Your script must use the yield generator

        Prototypes:
            def stream_users_in_batches(batch_size)
            def batch_processing(batch_size)

"""

from seed import connect_db


def stream_users_in_batches(batch_size: int):
    command = """SELECT * FROM user_data LIMIT %s"""

    with connect_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(command, (batch_size,))
            rows = cursor.fetchall()

            if rows:
                for row in rows:
                    yield row


def batch_processing():
    command = """SELECT * FROM user_data ud WHERE ud.age > 25"""

    with connect_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(command)
            rows = cursor.fetchall()

            if rows:
                for row in rows:
                    yield row


def main():
    for user in batch_processing():
        print(user)


if __name__ == "__main__":
    main()
