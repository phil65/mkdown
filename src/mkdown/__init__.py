"""mkdown: main package.

Tools for (Python-)Markdown.
"""

from __future__ import annotations

from importlib.metadata import version

__version__ = version("mkdown")
__title__ = "mkdown"

__author__ = "Philipp Temminghoff"
__author_email__ = "philipptemminghoff@googlemail.com"
__copyright__ = "Copyright (c) 2024 Philipp Temminghoff"
__license__ = "MIT"
__url__ = "https://github.com/phil65/mkdown"

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
    "__version__",
    "create_chunk_boundary",
    "create_image_reference",
    "create_metadata_comment",
    "create_page_break",
    "get_chunk_boundaries",
    "parse_metadata_comments",
    "split_markdown_by_chunks",
    "split_markdown_by_page",
]
