import os
from threading import Lock

import psycopg_pool
from dotenv import load_dotenv
from pgvector.psycopg import register_vector
from psycopg.rows import dict_row  # type: ignore

load_dotenv()

lock = Lock()

PGS_URL = os.environ.get("PGS_URL", None)
POOL = None

POSTGRES_HOST = os.environ.get("POSTGRES_HOST", None)
POSTGRES_USER = os.environ.get("POSTGRES_USER", None)
POSTGRES_PASS = os.environ.get("POSTGRES_PASSWORD", None)
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", None)
POSTGRES_DB = os.environ.get("POSTGRES_DB", None)

CONN_INFO = (
    f"host={POSTGRES_HOST} "
    + f"port={POSTGRES_PORT} "
    + f"dbname={POSTGRES_DB} "
    + f"user={POSTGRES_USER} "
    + f"password={POSTGRES_PASS}"
)


def get_pool(force_create=False) -> psycopg_pool.ConnectionPool:
    """Get a postgres connection."""
    global POOL  # noqa
    with lock:
        if POOL is None or force_create:
            POOL = psycopg_pool.ConnectionPool(
                CONN_INFO,
                open=False,
                min_size=1,
                max_size=10,
                max_idle=10,
                reconnect_timeout=10,
                max_lifetime=60,
                check=psycopg_pool.ConnectionPool.check_connection,
            )
            POOL.open()
            POOL.wait()
    return POOL


def db_query(query: str, args: dict | None = None, response=True) -> list[dict] | None:
    """Execute a database query using the connection pool.

    Args:
        query: The SQL query to execute.
        args: Arguments to be used with the query.

    Returns:
        List[tuple]: The query results.
    """
    with get_pool().connection() as conn:

        register_vector(conn)

        with conn.cursor(
            row_factory=dict_row,
        ) as cursor:
            cursor.execute(query, args)

            if response:
                return cursor.fetchall()
            else:
                return None
