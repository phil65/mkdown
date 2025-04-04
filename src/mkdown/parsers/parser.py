"""Main markdown parser integrating all types of processors."""

from __future__ import annotations

import importlib.util
from typing import TYPE_CHECKING, Any, ClassVar
import warnings

from mkdown.post_processors.registry import PostProcessorRegistry
from mkdown.pre_processors.registry import PreProcessorRegistry
from mkdown.tree_processors.registry import TreeProcessorRegistry


if TYPE_CHECKING:
    from mkdown.parsers.base_parser import BaseParser


LXML_AVAILABLE = importlib.util.find_spec("lxml") is not None


class MarkdownParser:
    """Markdown parser with support for pre/tree/post processors."""

    DEFAULT_RUST_PARSER: ClassVar[str] = "comrak"

    def __init__(
        self,
        rust_parser: str = "comrak",
        use_lxml: bool = True,
        unsafe: bool = False,
    ) -> None:
        """Initialize a markdown parser with configurable processors."""
        self.rust_parser = rust_parser
        self.use_lxml = use_lxml and LXML_AVAILABLE
        self.unsafe = unsafe

        # Initialize processor registries
        self.pre_processors = PreProcessorRegistry()
        self.tree_processors = TreeProcessorRegistry()
        self.post_processors = PostProcessorRegistry()

    def convert(self, markdown_text: str, **parser_options: Any) -> str:
        """Convert markdown to HTML using the configured processors."""
        # 1. Run pre-processors
        processed_markdown = self._apply_pre_processors(markdown_text)
        # 2. Convert markdown to HTML using selected Rust parser
        html = self._convert_markdown_to_html(processed_markdown, **parser_options)
        # 3. Run tree processors if needed
        html = self._apply_tree_processors(html)
        # 4. Run post-processors
        return self._apply_post_processors(html)

    def _apply_pre_processors(self, text: str) -> str:
        """Apply pre-processors to markdown text."""
        if not self.pre_processors.has_processors:
            return text

        result = text
        for processor in self.pre_processors.processors:
            result = processor.process_markdown(result)
        return result

    def _apply_tree_processors(self, html: str) -> str:
        """Apply tree processors to HTML."""
        if self.use_lxml and self.tree_processors.has_lxml_processors:
            return self._apply_lxml_processors(html)
        if self.tree_processors.has_et_processors:
            return self._apply_et_processors(html)
        return html

    def _apply_lxml_processors(self, html: str) -> str:
        """Apply lxml tree processors."""
        from lxml import etree as lxml_etree

        try:
            tree = lxml_etree.fromstring(f"<root>{html}</root>")

            for processor in self.tree_processors.lxml_processors:
                tree = processor.process_tree(tree)

            return "".join(
                lxml_etree.tostring(child, encoding="unicode") for child in tree
            )
        except Exception as e:  # noqa: BLE001
            warnings.warn(
                f"Error processing with lxml: {e}. Falling back to ElementTree.",
                stacklevel=2,
            )
            return self._apply_et_processors(html)

    def _apply_et_processors(self, html: str) -> str:
        """Apply ElementTree processors."""
        from xml.etree import ElementTree as ET

        if not self.tree_processors.has_et_processors:
            return html

        try:
            tree = ET.fromstring(f"<root>{html}</root>")

            for processor in self.tree_processors.et_processors:
                tree = processor.process_tree(tree)

            return "".join(ET.tostring(child, encoding="unicode") for child in tree)
        except Exception as e:  # noqa: BLE001
            warnings.warn(
                f"Error processing tree with ElementTree: {e}",
                stacklevel=2,
            )
            return html

    def _apply_post_processors(self, html: str) -> str:
        """Apply post-processors to HTML."""
        if not self.post_processors.has_processors:
            return html

        result = html
        for processor in self.post_processors.processors:
            result = processor.process_html(result)
        return result

    def _convert_markdown_to_html(self, markdown_text: str, **options: Any) -> str:
        """Convert markdown to HTML using the selected Rust parser."""
        match self.rust_parser:
            case "comrak":
                from mkdown.parsers.comrak_parser.parser import ComrakParser

                options.setdefault("unsafe_", self.unsafe)
                parser: BaseParser = ComrakParser(**options)
                return parser.convert(markdown_text)

            case "pyromark":
                from mkdown.parsers.pyromark_parser.parser import PyroMarkParser

                parser = PyroMarkParser(**options)
                return parser.convert(markdown_text)

            case "markdown-it-pyrs":
                from mkdown.parsers.markdown_it_pyrs_parser.parser import (
                    MarkdownItPyRSParser,
                )

                parser = MarkdownItPyRSParser(**options)
                return parser.convert(markdown_text)

        msg = f"Unsupported Rust parser: {self.rust_parser}"
        raise ValueError(msg)

        msg = f"Unsupported Rust parser: {self.rust_parser}"
        raise ValueError(msg)
