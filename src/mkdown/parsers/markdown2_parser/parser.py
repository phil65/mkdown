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

    def convert(self, markdown_text: str, **options: Any) -> str:
        """Convert markdown to HTML.

        Args:
            markdown_text: Input markdown text
            **options: Override default options

        Returns:
            HTML output as string
        """
        import markdown2

        # If options provided, create new parser with updated options
        if options:
            # Start with base options
            new_options = self._options.copy()
            extras = self._extras.copy()

            # Update extras based on common options
            option_mapping = {
                "tables": "tables",
                "footnotes": "footnotes",
                "strikethrough": "strike",
                "tasklist": "task_list",
                "tasklists": "task_list",
                "fenced_code": "fenced-code-blocks",
            }

            for opt_name, extra_name in option_mapping.items():
                if options.get(opt_name):
                    if extra_name not in extras:
                        extras.append(extra_name)
                elif opt_name in options and extra_name in extras:
                    extras.remove(extra_name)

            # Handle any additional extras
            if options.get("extras"):
                for extra in options["extras"]:
                    if extra not in extras:
                        extras.append(extra)

            # Update options
            new_options["extras"] = extras

            # Add any other options
            for key, value in options.items():
                if key not in option_mapping and key != "extras":
                    new_options[key] = value

            # Create new parser with updated options
            temp_parser = markdown2.Markdown(**new_options)
            return temp_parser.convert(markdown_text)

        # Use existing parser for efficiency
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
