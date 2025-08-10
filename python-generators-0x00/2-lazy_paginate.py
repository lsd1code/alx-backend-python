"""
#! Lazy loading Paginated Data

#? Objective: Simulate fetching paginated data from the users database using a generator to lazily load each page

Instructions:
    Implement a generator function lazypaginate(pagesize) that implements the paginate_users(page_size, offset) that will only fetch the next page when needed at an offset of 0.
        You must only use one loop
        Include the paginate_users function in your code
        You must use the yield generator
        Prototype:
        def lazy_paginate(page_size)
"""

from seed import connect_db


def lazypaginator(page_size: int):
    offset = 0

    def paginate_user(page_size: int, offset: int):
        command = """SELECT * FROM user_data OFFSET (%s) LIMIT (%s)"""

        with connect_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute(command, (offset, page_size))
                rows = cursor.fetchall()

                if rows:
                    for row in rows:
                        yield row

    return paginate_user(page_size, offset)


def main():
    for r in lazypaginator(2):
        print(r)


if __name__ == "__main__":
    main()
