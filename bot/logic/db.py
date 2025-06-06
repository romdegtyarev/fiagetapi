import asyncpg
import os


DATABASE_URL = os.getenv("DATABASE_URL")


_pool = None


async def get_pool():
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(DATABASE_URL)
    return _pool


async def create_users_table():
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id BIGINT PRIMARY KEY,
                username TEXT,
                date_added TIMESTAMPTZ DEFAULT now()
            );
        """)


async def add_user(user_id: int, username: str = ""):
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            "INSERT INTO users (user_id, username) VALUES ($1, $2) ON CONFLICT DO NOTHING;",
            user_id, username
        )


async def list_users():
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT user_id, username, date_added FROM users ORDER BY date_added DESC;")
        return rows


async def is_user_exists(user_id: int) -> bool:
    pool = await get_pool()
    async with pool.acquire() as conn:
        res = await conn.fetchval("SELECT 1 FROM users WHERE user_id=$1;", user_id)
        return bool(res)
