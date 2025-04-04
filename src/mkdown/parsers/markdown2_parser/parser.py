"""Markdown2 parser implementation."""

from __future__ import annotations

from typing import Any

from mkdown.parsers.base_parser import BaseParser


class Markdown2Parser(BaseParser):
    """Parser implementation using Markdown2."""

    def __init__(
        self,
        # Common feature options
        tables: bool = False,
        footnotes: bool = False,
        strikethrough: bool = False,
        tasklists: bool = False,
        fenced_code: bool = True,
        # Markdown2-specific options
        extras: list[str] | None = None,
        safe_mode: bool = False,
        html4tags: bool = False,
        header_ids: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initialize the Markdown2 parser.

        Args:
            tables: Enable tables extension
            footnotes: Enable footnotes extension
            strikethrough: Enable strikethrough extension
            tasklists: Enable tasklists extension
            fenced_code: Enable fenced code blocks
            extras: Additional Markdown2 extras to enable
            safe_mode: Enable safe mode
            html4tags: Output HTML4 tags
            header_ids: Add IDs to headers
            kwargs: Additional keyword arguments
        """
        import markdown2

        # Prepare extras list
        self._extras = extras or []

        # Add common features to extras
        if tables and "tables" not in self._extras:
            self._extras.append("tables")
        if footnotes and "footnotes" not in self._extras:
            self._extras.append("footnotes")
        if fenced_code and "fenced-code-blocks" not in self._extras:
            self._extras.append("fenced-code-blocks")
        if strikethrough and "strike" not in self._extras:
            self._extras.append("strike")
        if tasklists and "task_list" not in self._extras:
            self._extras.append("task_list")
        if header_ids and "header-ids" not in self._extras:
            self._extras.append("header-ids")

        # Store options
        self._options = {
            "extras": self._extras,
            "safe_mode": safe_mode,
            "html4tags": html4tags,
            **kwargs,
        }

        # Create parser instance
        self._parser = markdown2.Markdown(**self._options)

        # Store feature mappings for later use
        self._feature_mappings = {
            "tables": "tables",
            "footnotes": "footnotes",
            "fenced-code-blocks": "fenced_code",
            "strike": "strikethrough",
            "task_list": "tasklists",
        }

    def convert(self, markdown_text: str) -> str:
        """Convert markdown to HTML.

        Args:
            markdown_text: Input markdown text

        Returns:
            HTML output as string
        """
        return self._parser.convert(markdown_text)

    @property
    def name(self) -> str:
        """Get the name of the parser."""
        return "markdown2"

    @property
    def features(self) -> set[str]:
        """Get the set of supported features."""
        features = {"basic_markdown"}

        # Add features based on enabled extras
        for extra in self._extras:
            if extra in self._feature_mappings:
                features.add(self._feature_mappings[extra])

        return features


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.DEBUG)

    parser = Markdown2Parser()
    print(parser.convert("# Test"))
