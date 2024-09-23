from datetime import datetime
from enum import Enum

from pydantic import BaseModel
from pydantic import Field
from pydantic import RootModel


class BaseList(RootModel):
    """Utility class for list models."""

    def __hash__(self) -> int:
        return hash(self.model_dump_json())

    def __iter__(self):  # noqa
        return iter(self.root)

    def __getitem__(self, item):  # noqa
        return self.root[item]

    def __len__(self):  # noqa
        return len(self.root)


class AuthorOrder(Enum):
    FIRST = 0
    MIDDLE = 1
    LAST = 2


class IndexedModel(BaseModel):
    id_: int = Field(..., alias="id")


class Author(IndexedModel):
    name: str
    alex_aid: int


class Authorship(BaseModel):
    author_id: int
    works_id: int
    order: AuthorOrder


class Work(IndexedModel):
    alex_wid: int
    pub_date: datetime
    pmid: int
    source_id: int
    doi: str
    pdf: str


class Source(IndexedModel):
    alex_sid: int
    abbreviated_title: str
    country: str


class Chunk(IndexedModel):
    work_id: int
    text: str


class Embedding(IndexedModel):
    chunk_id: int
    embedding: list[float]
    distance: float | None = None


class EmbeddingList(BaseList):
    root: list[Embedding]


class Citation(BaseModel):
    """This models holds citation related information."""

    authors: list[Author]
    work: Work
    source: Source


class Passage(BaseModel):
    """This model holds a passage, an embedding, and citation information."""

    citation: Citation
    chunk: Chunk
    embedding: Embedding
