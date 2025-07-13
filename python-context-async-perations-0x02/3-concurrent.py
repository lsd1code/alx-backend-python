"""
#! Concurrent Asynchronous Database Queries

    #? Objective: Run multiple database queries concurrently using asyncio.gather.

Instructions:

    Use the aiosqlite library to interact with SQLite asynchronously. To learn more about it, click here.

    Write two asynchronous functions: async_fetch_users() and async_fetch_older_users() that fetches all users and users older than 40 respectively.

    Use the asyncio.gather() to execute both queries concurrently.

    Use asyncio.run(fetch_concurrently()) to run the concurrent fetch

    ! Users Table
    CREATE TABLE users (
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        age DECIMAL NOT NULL
    );
"""

import asyncio
import aiosqlite


async def async_fetch_users():
    async with aiosqlite.connect("users.db") as cursor:
        async with cursor.execute('SELECT * FROM users') as results:
            async for row in results:
                print(row)


async def async_fetch_older_users():
    async with aiosqlite.connect("users.db") as cursor:
        async with cursor.execute('SELECT * FROM users u WHERE u.age > 40;') as results:
            async for row in results:
                print(row)


async def fetch_concurrently():
    await asyncio.gather(
        async_fetch_users(), async_fetch_older_users())

if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
