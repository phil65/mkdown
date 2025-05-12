"""Markdown document models and utilities."""

from __future__ import annotations

__version__ = "0.13.2"


from mkdown.models.document import Document
from mkdown.models.textchunk import TextChunk
from mkdown.models.image import Image
from mkdown.markdown_utils import (
    CHUNK_BOUNDARY_TYPE,
    DEFAULT_PREFIX,
    PAGE_BREAK_TYPE,
    create_chunk_boundary,
    create_page_break,
    create_image_reference,
    create_metadata_comment,
    get_chunk_boundaries,
    parse_metadata_comments,
    split_markdown_by_chunks,
    split_markdown_by_page,
)


__all__ = [
    "CHUNK_BOUNDARY_TYPE",
    "DEFAULT_PREFIX",
    "PAGE_BREAK_TYPE",
    "Document",
    "Image",
    "TextChunk",
    "create_chunk_boundary",
    "create_image_reference",
    "create_metadata_comment",
    "create_page_break",
    "get_chunk_boundaries",
    "parse_metadata_comments",
    "split_markdown_by_chunks",
    "split_markdown_by_page",
]
