"""PyroMark parser implementation."""

from __future__ import annotations

from typing import Any

from mkdown.parsers.base_parser import BaseParser


class PyroMarkParser(BaseParser):
    """Parser implementation using PyroMark."""

    def __init__(
        self,
        # Feature options
        enable_tables: bool = False,
        enable_footnotes: bool = False,
        enable_strikethrough: bool = False,
        enable_tasklists: bool = False,
        enable_smart_punctuation: bool = False,
        enable_heading_attributes: bool = False,
        enable_yaml_style_metadata_blocks: bool = False,
        enable_pluses_delimited_metadata_blocks: bool = False,
        enable_old_footnotes: bool = False,
        enable_math: bool = False,
        enable_gfm: bool = True,  # Enable GFM by default
        enable_definition_list: bool = False,
        enable_superscript: bool = False,
        enable_subscript: bool = False,
        enable_wikilinks: bool = False,
        **kwargs: Any,
    ) -> None:
        """Initialize the PyroMark parser.

        Args:
            enable_tables: Enable tables extension
            enable_footnotes: Enable footnotes extension
            enable_strikethrough: Enable strikethrough extension
            enable_tasklists: Enable tasklists extension
            enable_smart_punctuation: Enable smart punctuation
            enable_heading_attributes: Enable heading attributes extension
            enable_yaml_style_metadata_blocks: Enable YAML-style metadata blocks
            enable_pluses_delimited_metadata_blocks: Enable plus-delimited metadata blocks
            enable_old_footnotes: Enable old footnotes style
            enable_math: Enable math extension
            enable_gfm: Enable GitHub Flavored Markdown (defaults to True)
            enable_definition_list: Enable definition lists
            enable_superscript: Enable superscript extension
            enable_subscript: Enable subscript extension
            enable_wikilinks: Enable wikilinks extension
            kwargs: Additional keyword arguments
        """
        from pyromark._options import Options

        # Build options flag
        self._options = Options(0)

        if enable_tables:
            self._options |= Options.ENABLE_TABLES
        if enable_footnotes:
            self._options |= Options.ENABLE_FOOTNOTES
        if enable_strikethrough:
            self._options |= Options.ENABLE_STRIKETHROUGH
        if enable_tasklists:
            self._options |= Options.ENABLE_TASKLISTS
        if enable_smart_punctuation:
            self._options |= Options.ENABLE_SMART_PUNCTUATION
        if enable_heading_attributes:
            self._options |= Options.ENABLE_HEADING_ATTRIBUTES
        if enable_yaml_style_metadata_blocks:
            self._options |= Options.ENABLE_YAML_STYLE_METADATA_BLOCKS
        if enable_pluses_delimited_metadata_blocks:
            self._options |= Options.ENABLE_PLUSES_DELIMITED_METADATA_BLOCKS
        if enable_old_footnotes:
            self._options |= Options.ENABLE_OLD_FOOTNOTES
        if enable_math:
            self._options |= Options.ENABLE_MATH
        if enable_gfm:
            self._options |= Options.ENABLE_GFM
        if enable_definition_list:
            self._options |= Options.ENABLE_DEFINITION_LIST
        if enable_superscript:
            self._options |= Options.ENABLE_SUPERSCRIPT
        if enable_subscript:
            self._options |= Options.ENABLE_SUBSCRIPT
        if enable_wikilinks:
            self._options |= Options.ENABLE_WIKILINKS

        # Store initial options for feature detection
        self._feature_options = {
            "tables": enable_tables,
            "footnotes": enable_footnotes,
            "strikethrough": enable_strikethrough,
            "tasklists": enable_tasklists,
            "smart_punctuation": enable_smart_punctuation,
            "heading_attributes": enable_heading_attributes,
            "yaml_metadata": enable_yaml_style_metadata_blocks,
            "plus_metadata": enable_pluses_delimited_metadata_blocks,
            "old_footnotes": enable_old_footnotes,
            "math": enable_math,
            "gfm": enable_gfm,
            "definition_list": enable_definition_list,
            "superscript": enable_superscript,
            "subscript": enable_subscript,
            "wikilinks": enable_wikilinks,
        }

        # Additional options
        self._kwargs = kwargs

    def convert(self, markdown_text: str, **options: Any) -> str:
        """Convert markdown to HTML.

        Args:
            markdown_text: Input markdown text
            **options: Override default options

        Returns:
            HTML output as string
        """
        import pyromark
        from pyromark._options import Options

        # If options provided, create updated options object
        if options:
            # Build new options flag
            new_options = Options(0)

            # Map common options to pyromark options
            option_mapping = {
                "table": "tables",
                "tables": "tables",
                "footnotes": "footnotes",
                "strikethrough": "strikethrough",
                "tasklist": "tasklists",
                "tasklists": "tasklists",
            }

            # Start with our stored feature options
            feature_options = self._feature_options.copy()

            # Apply any overrides
            for opt_name, feature_name in option_mapping.items():
                if opt_name in options:
                    feature_options[feature_name] = options[opt_name]

            # Apply direct overrides for any pyromark-specific option
            for opt_name in feature_options:
                if f"enable_{opt_name}" in options:
                    feature_options[opt_name] = options[f"enable_{opt_name}"]

            # Build the options flag
            if feature_options["tables"]:
                new_options |= Options.ENABLE_TABLES
            if feature_options["footnotes"]:
                new_options |= Options.ENABLE_FOOTNOTES
            if feature_options["strikethrough"]:
                new_options |= Options.ENABLE_STRIKETHROUGH
            if feature_options["tasklists"]:
                new_options |= Options.ENABLE_TASKLISTS
            if feature_options["smart_punctuation"]:
                new_options |= Options.ENABLE_SMART_PUNCTUATION
            if feature_options["heading_attributes"]:
                new_options |= Options.ENABLE_HEADING_ATTRIBUTES
            if feature_options["yaml_metadata"]:
                new_options |= Options.ENABLE_YAML_STYLE_METADATA_BLOCKS
            if feature_options["plus_metadata"]:
                new_options |= Options.ENABLE_PLUSES_DELIMITED_METADATA_BLOCKS
            if feature_options["old_footnotes"]:
                new_options |= Options.ENABLE_OLD_FOOTNOTES
            if feature_options["math"]:
                new_options |= Options.ENABLE_MATH
            if feature_options["gfm"]:
                new_options |= Options.ENABLE_GFM
            if feature_options["definition_list"]:
                new_options |= Options.ENABLE_DEFINITION_LIST
            if feature_options["superscript"]:
                new_options |= Options.ENABLE_SUPERSCRIPT
            if feature_options["subscript"]:
                new_options |= Options.ENABLE_SUBSCRIPT
            if feature_options["wikilinks"]:
                new_options |= Options.ENABLE_WIKILINKS

            # Convert to HTML using pyromark with new options
            return pyromark.html(markdown_text, options=new_options)

        # Use stored options for efficiency when no options are changed
        return pyromark.html(markdown_text, options=self._options)

    @property
    def name(self) -> str:
        """Get the name of the parser."""
        return "pyromark"

    @property
    def features(self) -> set[str]:
        """Get the set of supported features."""
        features = {"basic_markdown", "fenced_code"}

        # Add features based on enabled options
        if self._feature_options["tables"]:
            features.add("tables")
        if self._feature_options["footnotes"]:
            features.add("footnotes")
        if self._feature_options["strikethrough"]:
            features.add("strikethrough")
        if self._feature_options["tasklists"]:
            features.add("tasklists")
        if self._feature_options["math"]:
            features.add("math")
        if self._feature_options["gfm"]:
            features.add("gfm")
            features.add("alerts")  # GFM includes alerts
        if self._feature_options["definition_list"]:
            features.add("definition_list")
        if self._feature_options["superscript"]:
            features.add("superscript")
        if self._feature_options["subscript"]:
            features.add("subscript")
        if self._feature_options["wikilinks"]:
            features.add("wikilinks")

        return features


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.DEBUG)

    parser = PyroMarkParser()
    print(parser.convert("# Test"))
