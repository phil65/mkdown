"""Base classes for HTML sanitizers that clean HTML of dangerous content."""

from __future__ import annotations

from abc import ABC, abstractmethod


class HTMLSanitizer(ABC):
    """Abstract base class for HTML sanitizers."""

    def __init__(
        self,
        tags: set[str] | None = None,
        attributes: dict[str, set[str]] | None = None,
        protocols: set[str] | None = None,
        strip_comments: bool = True,
    ) -> None:
        """Initialize with common sanitization options.

        Args:
            tags: HTML tags to allow (None for default)
            attributes: HTML attributes to allow (None for default)
            protocols: URL protocols to allow (None for default)
            strip_comments: Whether to strip HTML comments
        """
        self.tags = tags
        self.attributes = attributes
        self.protocols = protocols
        self.strip_comments = strip_comments

    @abstractmethod
    def sanitize(self, html: str) -> str:
        """Sanitize HTML content to remove potentially dangerous elements.

        Args:
            html: The HTML content to sanitize

        Returns:
            The sanitized HTML content
        """
        ...
