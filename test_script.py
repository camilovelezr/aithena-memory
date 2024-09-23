import random

import numpy as np

from aithena.memory.postgres import tables
from aithena.memory.postgres.query import insert_embedding
from aithena.memory.postgres.query import vector_search

CLEANUP = True
EMBEDDING_TABLE_NAME = "dummy"

# Enable the vector table extension
tables.create_extension()

# Create the tables
tables.create_author_table()
tables.create_authorship_table()
tables.create_chunk_table()
tables.create_embedding_table(model_name="dummy", dims=128)
tables.create_embedding_index(model_name="dummy")
tables.create_source_table()
tables.create_work_table()

# Create a few dummy embeddings
for _ in range(10):
    embedding = np.random.rand(128)
    chunk_id = 0

    # Insert the dummy embedding
    embedding = insert_embedding(
        table_name="dummy", embedding=embedding, chunk_id=chunk_id
    )

# Do a vector search
embedding = np.random.rand(128)
embeddings = vector_search(model_name="dummy", embedding=embedding, k=3)

print([(e.id_, e.distance) for e in embeddings])

# Remove the tables
if CLEANUP:
    tables.drop_author_table()
    tables.drop_authorship_table()
    tables.drop_chunk_table()
    tables.drop_embedding_table(table_name="dummy")
    tables.drop_embedding_index(model_name="dummy")
    tables.drop_source_table()
    tables.drop_work_table()
