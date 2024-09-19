from aithena.memory.postgres.utils import db_query
from aithena.memory.models import Embedding


def insert_embedding(
    table_name: str, embedding: list[float], chunk_id: int
) -> Embedding:
    """"""

    query = f"""
INSERT INTO {table_name} (chunk_id, embedding) VALUES (
    %(chunk_id)s,
    %(embedding)s
)
RETURNING id"""

    result = db_query(query, {"embedding": embedding, "chunk_id": chunk_id})[0]

    assert result is not None

    return Embedding(id=result["id"], embedding=embedding, chunk_id=chunk_id)
