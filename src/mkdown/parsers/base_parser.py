"""Base classes for markdown parsers."""

from __future__ import annotations

from abc import ABC, abstractmethod


class BaseParser(ABC):
    """Abstract base class for markdown parsers."""

    @abstractmethod
    def convert(self, markdown_text: str) -> str:
        """Convert markdown to HTML.

        Args:
            markdown_text: Input markdown text
            **options: Parser-specific options

        Returns:
            HTML output as string
        """

    @property
    @abstractmethod
    def name(self) -> str:
        """Get the name of the parser."""

    @property
    @abstractmethod
    def features(self) -> set[str]:
        """Get the set of supported features."""
