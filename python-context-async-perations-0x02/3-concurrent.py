import asyncio
import aiosqlite

DB_NAME = "axl_backend.db"

async def async_fetch_users():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            rows = await cursor.fetchall()
            return rows  

async def async_fetch_older_users():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            rows = await cursor.fetchall()
            return rows  

async def fetch_concurrently():
    users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

    print("All Users:")
    for row in users:
        print(row)

    print("\nUsers older than 40:")
    for row in older_users:
        print(row)

if __name__ == "__main__":
    asyncio.run(fetch_concurre
