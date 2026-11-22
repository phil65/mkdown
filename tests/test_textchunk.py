"""Tests for the TextChunk model."""

from __future__ import annotations

from pydantic import BaseModel, TypeAdapter

from mkdown import Image, TextChunk


class ChunkContainer(BaseModel):
    chunks: list[TextChunk]


def test_textchunk_usable_in_pydantic_model_without_rebuild():
    """A model nesting TextChunk must be fully defined without model_rebuild()."""
    image = Image(id="img-1", content=b"data", mime_type="image/png")
    chunk = TextChunk(content="text", source_doc_id="doc", chunk_index=0, images=[image])
    container = ChunkContainer(chunks=[chunk])
    assert container.chunks[0].images[0].id == "img-1"

    restored = ChunkContainer.model_validate_json(container.model_dump_json())
    assert restored.chunks[0].content == "text"
    assert isinstance(restored.chunks[0].images[0], Image)


def test_textchunk_type_adapter():
    adapter = TypeAdapter(TextChunk)
    chunk = adapter.validate_python({"content": "a", "source_doc_id": "d", "chunk_index": 1})
    assert chunk.images == []


def test_to_numbered_text():
    chunk = TextChunk(content="a\nb", source_doc_id="d", chunk_index=0, metadata={"start_line": 3})
    assert chunk.to_numbered_text() == "    3 | a\n    4 | b"
