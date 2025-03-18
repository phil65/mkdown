"""Markdown-it-pyrs parser implementation."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from mkdown.parsers.base_parser import BaseParser


if TYPE_CHECKING:
    from markdown_it_pyrs.markdown_it_pyrs import _PLUGIN_NAME


class MarkdownItPyRSParser(BaseParser):
    """Parser implementation using markdown-it-pyrs."""

    def __init__(
        self,
        # Configuration preset
        config: Literal["commonmark", "gfm", "zero"] = "commonmark",
        # Common feature options
        tables: bool = False,
        footnotes: bool = False,
        strikethrough: bool = False,
        tasklists: bool = False,
        # Parser-specific options
        xhtml: bool = True,
        plugins: list[_PLUGIN_NAME] | None = None,
        **kwargs: Any,
    ) -> None:
        """Initialize the markdown-it-pyrs parser.

        Args:
            config: Configuration preset name
            tables: Enable tables extension
            footnotes: Enable footnotes extension
            strikethrough: Enable strikethrough extension
            tasklists: Enable tasklists extension
            xhtml: If true, use self-closing tags with trailing slash
            plugins: Additional plugins to enable
            kwargs: Additional keyword arguments
        """
        try:
            from markdown_it_pyrs import MarkdownIt
        except ImportError as e:
            msg = (
                "markdown-it-pyrs is not installed. Install it with "
                "'pip install markdown-it-pyrs'."
            )
            raise ImportError(msg) from e

        # Store base configuration
        self._config = config
        self._xhtml = xhtml

        # Initialize parser with configuration preset
        self._parser = MarkdownIt(config)

        # Store enabled plugins for feature detection
        self._enabled_plugins = set()

        # Enable plugins based on feature flags if not part of current config
        # GFM preset already includes tables and strikethrough
        if config != "gfm":
            if tables:
                self._parser.enable("table")
                self._enabled_plugins.add("table")
            if strikethrough:
                self._parser.enable("strikethrough")
                self._enabled_plugins.add("strikethrough")

        # These need to be explicitly enabled for any preset
        if footnotes:
            self._parser.enable("footnote")
            self._enabled_plugins.add("footnote")
        if tasklists:
            self._parser.enable("tasklist")
            self._enabled_plugins.add("tasklist")

        # Add any additional plugins
        if plugins:
            self._parser.enable_many(plugins)
            self._enabled_plugins.update(plugins)

    def convert(self, markdown_text: str, **options: Any) -> str:
        """Convert markdown to HTML.

        Args:
            markdown_text: Input markdown text
            **options: Override default options

        Returns:
            HTML output as string
        """
        try:
            from markdown_it_pyrs import MarkdownIt
        except ImportError as e:
            msg = (
                "markdown-it-pyrs is not installed. Install it with "
                "'pip install markdown-it-pyrs'."
            )
            raise ImportError(msg) from e

        # Handle options that might be passed
        xhtml = options.get("xhtml", self._xhtml)

        # If plugins or config are provided, create a new parser instance
        if "config" in options or "plugins" in options:
            config = options.get("config", self._config)

            # Create new parser
            temp_parser = MarkdownIt(config)

            # Enable specified plugins
            if options.get("plugins"):
                temp_parser.enable_many(options["plugins"])

            # Handle common feature options
            feature_plugin_map: dict[str, _PLUGIN_NAME] = {
                "table": "table",
                "tables": "table",
                "footnotes": "footnote",
                "footnote": "footnote",
                "strikethrough": "strikethrough",
                "tasklist": "tasklist",
                "tasklists": "tasklist",
            }

            # Enable plugins based on feature flags
            for feature, plugin in feature_plugin_map.items():
                if options.get(feature, False):
                    temp_parser.enable(plugin)

            # Render with the temporary parser
            return temp_parser.render(markdown_text, xhtml=xhtml)

        # Use the existing parser for efficiency
        return self._parser.render(markdown_text, xhtml=xhtml)

    @property
    def name(self) -> str:
        """Get the name of the parser."""
        return "markdown-it-pyrs"

    @property
    def features(self) -> set[str]:
        """Get the set of supported features."""
        # Basic features that are always supported
        features = {"basic_markdown", "fenced_code"}

        # Features based on configuration preset
        if self._config in ("commonmark", "gfm"):
            features.update({
                "blockquote",
                "code",
                "heading",
                "link",
                "image",
                "emphasis",
            })

        if self._config == "gfm":
            features.update({"tables", "strikethrough", "autolink"})

        # Features based on explicitly enabled plugins
        plugin_feature_map = {
            "table": "tables",
            "footnote": "footnotes",
            "strikethrough": "strikethrough",
            "tasklist": "tasklists",
            "autolink_ext": "autolink",
            "heading_anchors": "header_ids",
            "deflist": "definition_lists",
        }

        for plugin in self._enabled_plugins:
            if plugin in plugin_feature_map:
                features.add(plugin_feature_map[plugin])

        return features


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.DEBUG)

    parser = MarkdownItPyRSParser()
    print(parser.convert("# Test"))
