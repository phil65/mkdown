"""Marko parser implementation."""

from __future__ import annotations

from typing import Any

from mkdown.parsers.base_parser import BaseParser


class MarkoParser(BaseParser):
    """Parser implementation using Marko."""

    def __init__(
        self,
        # Common feature options
        tables: bool = False,
        footnotes: bool = False,
        strikethrough: bool = False,
        tasklists: bool = False,
        # Marko-specific options
        gfm: bool = False,
        pangu: bool = False,
        codehilite: bool = False,
        toc: bool = False,
        **kwargs: Any,
    ) -> None:
        """Initialize the Marko parser.

        Args:
            tables: Enable tables extension (used only if gfm=False)
            footnotes: Enable footnotes extension
            strikethrough: Enable strikethrough extension (used only if gfm=False)
            tasklists: Enable tasklists/task_list extension (used only if gfm=False)
            gfm: Use GitHub Flavored Markdown (includes tables, strikethrough, tasklists)
            pangu: Enable pangu extension for CJK text spacing
            codehilite: Enable code highlighting with Pygments
            toc: Enable table of contents extension
            kwargs: Additional keyword arguments
        """
        try:
            import marko
        except ImportError as e:
            msg = "Marko is not installed. Install it with 'pip install marko'."
            raise ImportError(msg) from e

        # Store feature flags
        self._features = {
            "gfm": gfm,
            "footnotes": footnotes,
            "pangu": pangu,
            "codehilite": codehilite,
            "toc": toc,
        }

        # Build extensions list
        self._extensions = []

        if not gfm:
            # Only add these if not using GFM (which includes them already)
            if tables:
                self._extensions.append("tables")
            if strikethrough:
                self._extensions.append("strikethrough")
            if tasklists:
                self._extensions.append("tasklist")

        if footnotes:
            self._extensions.append("footnote")
        if pangu:
            self._extensions.append("pangu")
        if codehilite:
            self._extensions.append("codehilite")
        if toc:
            self._extensions.append("toc")

        self._parser = marko.Markdown(extensions=self._extensions)
        if gfm:
            from marko.ext.gfm import GFM

            self._parser.use(GFM)

    def convert(self, markdown_text: str, **kwargs) -> str:
        """Convert markdown to HTML.

        Args:
            markdown_text: Input markdown text
            **kwargs: Additional keyword arguments

        Returns:
            HTML output as string
        """
        if kwargs:
            parser = MarkoParser(**kwargs)
            return parser.convert(markdown_text)
        return self._parser.convert(markdown_text)

    @property
    def name(self) -> str:
        """Get the name of the parser."""
        return "marko"

    @property
    def features(self) -> set[str]:
        """Get the set of supported features."""
        # Basic features always available
        features = {"basic_markdown", "fenced_code"}

        # Features based on GFM
        if self._features["gfm"]:
            features.update({"tables", "strikethrough", "tasklists", "autolink"})

        # Features based on extensions
        for ext in self._extensions:
            if ext == "tables":
                features.add("tables")
            elif ext == "footnote":
                features.add("footnotes")
            elif ext == "strikethrough":
                features.add("strikethrough")
            elif ext == "tasklist":
                features.add("tasklists")
            elif ext == "pangu":
                features.add("pangu")
            elif ext == "codehilite":
                features.add("code_highlighting")
            elif ext == "toc":
                features.add("toc")

        return features


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.DEBUG)

    parser = MarkoParser()
    print(parser.convert("# Test"))
