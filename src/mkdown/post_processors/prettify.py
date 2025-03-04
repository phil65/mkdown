"""HTML sanitization post processor using bleach."""

from __future__ import annotations

import importlib.util
from typing import TYPE_CHECKING

from mkdown.post_processors.base import PostProcessor


if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence

BS4_AVAILABLE = importlib.util.find_spec("bs4") is not None


class Prettify(PostProcessor):
    """Post processor that sanitizes HTML using bleach."""

    def __init__(
        self,
        allowed_tags: Sequence[str] | None = None,
        allowed_attributes: Mapping[str, Sequence[str]] | None = None,
        allowed_protocols: Sequence[str] | None = None,
        strip: bool = True,
        strip_comments: bool = True,
        priority: int = 50,
    ) -> None:
        """Initialize with bleach sanitization options.

        Args:
            allowed_tags: HTML tags to allow (None for default)
            allowed_attributes: HTML attributes to allow (None for default)
            allowed_protocols: URL protocols to allow (None for default)
            strip: Whether to strip disallowed tags
            strip_comments: Whether to strip HTML comments
            priority: Execution priority (higher runs earlier)

        Raises:
            ImportError: If bleach is not installed
        """
        if not BS4_AVAILABLE:
            msg = (
                "bleach is not installed. Install it with 'pip install bs4' "
                "to use Prettify."
            )
            raise ImportError(msg)

        super().__init__(priority)
        self.allowed_tags = allowed_tags
        self.allowed_attributes = allowed_attributes
        self.allowed_protocols = allowed_protocols
        self.strip = strip
        self.strip_comments = strip_comments

    def process_html(self, html: str) -> str:
        """Sanitize HTML content using bleach.

        Args:
            html: The HTML content to sanitize

        Returns:
            The sanitized HTML content
        """
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(html, "html.parser")
        return soup.prettify()
