import hashlib
from pathlib import Path
from typing import AsyncIterator
import aiosqlite
import sqlite3

from aiohttp import web


def get_db_path() -> Path:
    here = Path.cwd()
    while not (here / ".git").exists():
        if here == here.parent:
            raise RuntimeError("Cannot find root github dir")
        here = here.parent

    return here / "db.sqlite3"


async def init_db(app: web.Application) -> AsyncIterator[None]:
    sqlite_db = get_db_path()
    db = await aiosqlite.connect(sqlite_db)
    db.row_factory = aiosqlite.Row
    app["DB"] = db
    yield
    await db.close()


async def fetch_user(
        db: aiosqlite.Connection,
        username: str,
        hashed_password: str
):
    async with db.execute(
            "SELECT username, secret_data FROM users WHERE username = ? and password = ?",
            [username, hashed_password]
    ) as cursor:
        row = await cursor.fetchone()
        if row is None:
            return False
        else:
            return {
                'username': row.get('username', None),
                'secret_data': row.get('secret_data', None)
            }


def try_make_db() -> None:
    sqlite_db = get_db_path()
    if sqlite_db.exists():
        return

    with sqlite3.connect(sqlite_db) as conn:
        cur = conn.cursor()
        cur.execute(
            """CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password CHAR(64),
            secret_data TEXT,
            )
        """
        )
        login = 'whom'
        password_not_hashed = '12344321qwe'
        password_hashed = hashlib.sha256(password_not_hashed.encode()).hexdigest()
        cur.execute(
            """INSERT INTO users (username, password, secret_data) VALUES (%s, %s, %s)""",
            (login, password_hashed, 'I love cookies!')
        )

        conn.commit()
