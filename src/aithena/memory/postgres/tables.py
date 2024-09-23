from aithena.memory.postgres.utils import db_query


def create_extension() -> None:
    """Create vector extension if it doesn't exist. Safe to call multiple times."""

    db_query("CREATE EXTENSION IF NOT EXISTS vector", response=False)


def create_author_table() -> None:
    """Create a vector table."""
    query = """
CREATE TABLE IF NOT EXISTS author (
    id bigserial PRIMARY KEY,
    alex_aid bigint,
    name text
)
"""
    db_query(query, response=False)


def create_authorship_table() -> None:
    """Create a vector table."""
    query = """
CREATE TABLE IF NOT EXISTS authorship (
    author_id bigint,
    works_id bigint,
    "order" smallint
)
"""
    db_query(query, response=False)


def create_work_table() -> None:
    """Create a vector table."""
    query = """
CREATE TABLE IF NOT EXISTS work (
    id bigserial PRIMARY KEY,
    alex_wid bigint,
    pub_date date,
    pmid int,
    source_id bigint,
    doi text,
    pdf text
)
"""
    db_query(query, response=False)


def create_source_table() -> None:
    """Create a vector table."""
    query = """
CREATE TABLE IF NOT EXISTS source (
    id bigserial PRIMARY KEY,
    alex_sid bigint,
    abbreviated_title text,
    country text
)
"""
    db_query(query, response=False)


def create_chunk_table() -> None:
    """Create a vector table."""
    query = """
CREATE TABLE IF NOT EXISTS chunk (
    id bigserial PRIMARY KEY,
    work_id bigint,
    text text
)
"""
    db_query(query, response=False)


def create_embedding_table(model_name: str, dims: int) -> None:
    """Create a vector table."""
    query = f"""
CREATE TABLE IF NOT EXISTS {model_name} (
    id bigserial PRIMARY KEY,
    chunk_id bigint,
    embedding vector({dims})
)
"""
    db_query(query, response=False)


def create_embedding_index(model_name: str) -> None:
    """Create a vector index."""
    query = f"""
CREATE INDEX IF NOT EXISTS embedding_index ON {model_name} USING hnsw (embedding vector_l2_ops)
"""

    db_query(query, response=False)


def drop_embedding_index(model_name: str) -> None:
    """Drop a vector index."""
    query = f"""
DROP INDEX IF EXISTS embedding_index
"""

    db_query(query, response=False)


def _drop_table(table: str):

    db_query(f"DROP TABLE IF EXISTS {table}", response=False)


def drop_author_table():
    _drop_table("author")


def drop_authorship_table():
    _drop_table("authorship")


def drop_chunk_table():
    _drop_table("chunk")


def drop_embedding_table(table_name: str):

    db_query(f"DROP TABLE IF EXISTS {table_name}", response=False)


def drop_source_table():
    _drop_table("source")


def drop_work_table():
    _drop_table("work")
