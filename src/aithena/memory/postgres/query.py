from aithena.memory.postgres.utils import db_query
from aithena.memory.models import Embedding
from aithena.memory.models import EmbeddingList


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

    result = db_query(query, {"embedding": embedding, "chunk_id": chunk_id})

    assert result is not None

    return Embedding(id=result[0]["id"], embedding=embedding, chunk_id=chunk_id)


def vector_search(model_name: str, embedding: list[float], k: int = 3) -> EmbeddingList:
    """Do an L2 search on a vector table."""

    query = f"""
SELECT 
    id,
    chunk_id,
    embedding,
    embedding <-> %(embedding)s as distance
FROM {model_name}
ORDER BY %(embedding)s <-> embedding ASC
LIMIT %(k)s
"""

    result = db_query(query, {"embedding": embedding, "k": k})

    assert result is not None

    return EmbeddingList.model_validate(result)
