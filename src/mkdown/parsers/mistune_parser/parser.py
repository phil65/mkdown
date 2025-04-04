"""Mistune parser implementation."""

from __future__ import annotations

from typing import Any

from mkdown.parsers.base_parser import BaseParser


class MistuneParser(BaseParser):
    """Parser implementation using Mistune."""

    def __init__(
        self,
        # Common feature options
        tables: bool = False,
        footnotes: bool = False,
        strikethrough: bool = False,
        tasklists: bool = False,
        # Mistune-specific options
        escape: bool = True,
        use_plugins: bool = True,
        plugins: list[str] | None = None,
        **kwargs: Any,
    ) -> None:
        """Initialize the Mistune parser.

        Args:
            tables: Enable tables extension
            footnotes: Enable footnotes extension
            strikethrough: Enable strikethrough extension
            tasklists: Enable tasklists extension
            escape: Escape HTML
            use_plugins: Use plugins
            plugins: List of plugins to use
            kwargs: Additional keyword arguments
        """
        import mistune  # pyright: ignore

        # Store feature flags
        self._features = {
            "tables": tables,
            "footnotes": footnotes,
            "strikethrough": strikethrough,
            "tasklists": tasklists,
        }

        # Initialize plugins list
        self._plugins = []

        if use_plugins:
            # Add built-in plugins based on feature flags
            if tables:
                self._plugins.append("table")
            if footnotes:
                self._plugins.append("footnotes")
            if strikethrough:
                self._plugins.append("strikethrough")
            if tasklists:
                self._plugins.append("task_lists")

            # Add additional plugins
            if plugins:
                for plugin in plugins:
                    if plugin not in self._plugins:
                        self._plugins.append(plugin)

        # Create the parser
        self._parser = mistune.create_markdown(
            escape=escape, plugins=self._plugins, **kwargs
        )

        # Store initialization options
        self._options = {"escape": escape, "plugins": self._plugins, **kwargs}

    def convert(self, markdown_text: str) -> str:
        """Convert markdown to HTML.

        Args:
            markdown_text: Input markdown text
            **options: Override default options

        Returns:
            HTML output as string
        """
        result = self._parser(markdown_text)
        return str(result)

    @property
    def name(self) -> str:
        """Get the name of the parser."""
        return "mistune"

    @property
    def features(self) -> set[str]:
        """Get the set of supported features."""
        features = {"basic_markdown", "fenced_code"}  # Mistune supports these by default

        # Add features based on enabled plugins
        plugin_feature_map = {
            "table": "tables",
            "footnotes": "footnotes",
            "strikethrough": "strikethrough",
            "task_lists": "tasklists",
        }

        for plugin in self._plugins:
            if plugin in plugin_feature_map:
                features.add(plugin_feature_map[plugin])

        return features


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.DEBUG)

    parser = MistuneParser()
    print(parser.convert("# Test"))
