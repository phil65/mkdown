"""Factory for creating HTML to Markdown converters."""

from __future__ import annotations

import importlib.util
from typing import TYPE_CHECKING, Any, Literal


if TYPE_CHECKING:
    from collections.abc import Callable

    from mkdown.html_to_md.base import (
        BaseHtmlToMarkdown,
        CodeBlockStyle,
        CodeFenceStyle,
        EmphasisStyle,
        HeadingStyle,
        HorizontalRuleStyle,
        LineBreakStyle,
        LinkStyle,
        ListMarkerStyle,
    )
    from mkdown.html_to_md.htmd_converter import HtmdConverter
    from mkdown.html_to_md.markdownify_converter import MarkdownifyConverter


# Check for library availability
HTMD_AVAILABLE = importlib.util.find_spec("htmd") is not None
MARKDOWNIFY_AVAILABLE = importlib.util.find_spec("markdownify") is not None


class HtmlToMarkdownFactory:
    """Factory for creating HTML to Markdown converters with consistent options."""

    @staticmethod
    def create(
        backend: Literal["auto", "htmd", "markdownify"] = "auto",
        # Common shared options
        heading_style: HeadingStyle | None = None,
        link_style: LinkStyle | None = None,
        code_block_style: CodeBlockStyle | None = None,
        code_fence_style: CodeFenceStyle | None = None,
        list_marker_style: ListMarkerStyle | None = None,
        line_break_style: LineBreakStyle | None = None,
        hr_style: HorizontalRuleStyle | None = None,
        emphasis_style: EmphasisStyle | None = None,
        skip_tags: list[str] | None = None,
        # Backend-specific options can be passed as additional kwargs
        **options: Any,
    ) -> BaseHtmlToMarkdown:
        """Create an HTML to Markdown converter with consistent options.

        Args:
            backend: Which backend to use ('auto', 'htmd', or 'markdownify')
            heading_style: Style for headings
            link_style: Style for links
            code_block_style: Style for code blocks
            code_fence_style: Style for code fences
            list_marker_style: Style for bullet list markers
            line_break_style: Style for line breaks
            hr_style: Style for horizontal rules
            emphasis_style: Style for emphasis
            skip_tags: HTML tags to skip during conversion
            **options: Backend-specific options

        Returns:
            An HTML to Markdown converter

        Raises:
            ImportError: If the requested backend is not available
            ValueError: If no suitable backend is available
        """
        # Combine standard options and backend-specific options
        combined_options = {
            "heading_style": heading_style,
            "link_style": link_style,
            "code_block_style": code_block_style,
            "code_fence_style": code_fence_style,
            "list_marker_style": list_marker_style,
            "line_break_style": line_break_style,
            "hr_style": hr_style,
            "emphasis_style": emphasis_style,
            "skip_tags": skip_tags,
            **options,
        }

        # Clean None values
        clean_options = {k: v for k, v in combined_options.items() if v is not None}

        # Try htmd (Rust-based, faster)
        if backend == "htmd" or (backend == "auto" and HTMD_AVAILABLE):
            from mkdown.html_to_md.htmd_converter import HtmdConverter

            return HtmdConverter(**clean_options)

        # Try markdownify (pure Python)
        if backend == "markdownify" or (backend == "auto" and MARKDOWNIFY_AVAILABLE):
            from mkdown.html_to_md.markdownify_converter import MarkdownifyConverter

            return MarkdownifyConverter(**clean_options)

        # No suitable backend found
        if backend == "auto":
            msg = (
                "No HTML to Markdown converter is available. "
                "Install either 'htmd-py' (recommended, Rust-based) or "
                "'markdownify' (pure Python)."
            )
            raise ValueError(msg)

        msg = (
            f"The requested backend '{backend}' is not available. "
            f"Install the corresponding package: "
            f"{'htmd-py' if backend == 'htmd' else 'markdownify'}."
        )
        raise ImportError(msg)

    @staticmethod
    def create_htmd(
        # Common shared options
        heading_style: HeadingStyle | None = None,
        link_style: LinkStyle | None = None,
        code_block_style: CodeBlockStyle | None = None,
        code_fence_style: CodeFenceStyle | None = None,
        list_marker_style: ListMarkerStyle | None = None,
        line_break_style: LineBreakStyle | None = None,
        hr_style: HorizontalRuleStyle | None = None,
        emphasis_style: EmphasisStyle | None = None,
        skip_tags: list[str] | None = None,
        # htmd-specific options
        preformatted_code: bool = False,
        **options: Any,
    ) -> HtmdConverter:
        """Create an HTML to Markdown converter using htmd.

        Args:
            heading_style: Style for headings
            link_style: Style for links
            code_block_style: Style for code blocks
            code_fence_style: Style for code fences
            list_marker_style: Style for bullet list markers
            line_break_style: Style for line breaks
            hr_style: Style for horizontal rules
            emphasis_style: Style for emphasis (not used by htmd)
            skip_tags: HTML tags to skip during conversion
            preformatted_code: Whether to preserve whitespace in code
            **options: Additional htmd-specific options

        Returns:
            An HTML to Markdown converter using htmd

        Raises:
            ImportError: If htmd is not installed
        """
        from mkdown.html_to_md.htmd_converter import HtmdConverter

        return HtmdConverter(
            heading_style=heading_style,
            link_style=link_style,
            code_block_style=code_block_style,
            code_fence_style=code_fence_style,
            list_marker_style=list_marker_style,
            line_break_style=line_break_style,
            hr_style=hr_style,
            emphasis_style=emphasis_style,
            skip_tags=skip_tags,
            preformatted_code=preformatted_code,
            **options,
        )

    @staticmethod
    def create_markdownify(
        # Common shared options
        heading_style: HeadingStyle | None = None,
        link_style: LinkStyle | None = None,
        code_block_style: CodeBlockStyle | None = None,
        code_fence_style: CodeFenceStyle | None = None,
        list_marker_style: ListMarkerStyle | None = None,
        line_break_style: LineBreakStyle | None = None,
        hr_style: HorizontalRuleStyle | None = None,
        emphasis_style: EmphasisStyle | None = None,
        skip_tags: list[str] | None = None,
        # Markdownify-specific options
        convert: list[str] | None = None,
        autolinks: bool = True,
        default_title: bool = False,
        sub_symbol: str = "",
        sup_symbol: str = "",
        code_language: str = "",
        code_language_callback: Callable | None = None,
        escape_asterisks: bool = True,
        escape_underscores: bool = True,
        escape_misc: bool = False,
        keep_inline_images_in: list[str] | None = None,
        table_infer_header: bool = False,
        wrap: bool = False,
        wrap_width: int | None = 80,
        strip_document: str | None = "STRIP",
        **options: Any,
    ) -> MarkdownifyConverter:
        """Create an HTML to Markdown converter using markdownify.

        Args:
            heading_style: Style for headings
            link_style: Style for links (not directly used by markdownify)
            code_block_style: Style for code blocks (not directly used by markdownify)
            code_fence_style: Style for code fences (not directly used by markdownify)
            list_marker_style: Style for bullet list markers
            line_break_style: Style for line breaks
            hr_style: Style for horizontal rules (not directly used by markdownify)
            emphasis_style: Style for emphasis
            skip_tags: HTML tags to skip during conversion
            convert: HTML tags to convert (alternative to skip_tags)
            autolinks: Use automatic link style for matching URLs
            default_title: Set title of links to href when no title is given
            sub_symbol: Symbol for subscripts
            sup_symbol: Symbol for superscripts
            code_language: Default language for code blocks
            code_language_callback: Callback to extract code language
            escape_asterisks: Whether to escape asterisks in text
            escape_underscores: Whether to escape underscores in text
            escape_misc: Whether to escape miscellaneous punctuation
            keep_inline_images_in: Tags that can contain inline images
            table_infer_header: Infer table headers from first row
            wrap: Whether to wrap text
            wrap_width: Width to wrap text at
            strip_document: How to strip document (LSTRIP, RSTRIP, STRIP, None)
            **options: Additional markdownify-specific options

        Returns:
            An HTML to Markdown converter using markdownify

        Raises:
            ImportError: If markdownify is not installed
        """
        from mkdown.html_to_md.markdownify_converter import MarkdownifyConverter

        return MarkdownifyConverter(
            heading_style=heading_style,
            link_style=link_style,
            code_block_style=code_block_style,
            code_fence_style=code_fence_style,
            list_marker_style=list_marker_style,
            line_break_style=line_break_style,
            hr_style=hr_style,
            emphasis_style=emphasis_style,
            skip_tags=skip_tags,
            convert=convert,
            autolinks=autolinks,
            default_title=default_title,
            sub_symbol=sub_symbol,
            sup_symbol=sup_symbol,
            code_language=code_language,
            code_language_callback=code_language_callback,
            escape_asterisks=escape_asterisks,
            escape_underscores=escape_underscores,
            escape_misc=escape_misc,
            keep_inline_images_in=keep_inline_images_in,
            table_infer_header=table_infer_header,
            wrap=wrap,
            wrap_width=wrap_width,
            strip_document=strip_document,
            **options,
        )


# Convenience function
def create_html_to_markdown(
    backend: Literal["auto", "htmd", "markdownify"] = "auto",
    # Common shared options
    heading_style: HeadingStyle | None = None,
    link_style: LinkStyle | None = None,
    code_block_style: CodeBlockStyle | None = None,
    code_fence_style: CodeFenceStyle | None = None,
    list_marker_style: ListMarkerStyle | None = None,
    line_break_style: LineBreakStyle | None = None,
    hr_style: HorizontalRuleStyle | None = None,
    emphasis_style: EmphasisStyle | None = None,
    skip_tags: list[str] | None = None,
    # Backend-specific options can be passed as additional kwargs
    **options: Any,
) -> BaseHtmlToMarkdown:
    """Create an HTML to Markdown converter with consistent options.

    Args:
        backend: Which backend to use ('auto', 'htmd', or 'markdownify')
        heading_style: Style for headings
        link_style: Style for links
        code_block_style: Style for code blocks
        code_fence_style: Style for code fences
        list_marker_style: Style for bullet list markers
        line_break_style: Style for line breaks
        hr_style: Style for horizontal rules
        emphasis_style: Style for emphasis
        skip_tags: HTML tags to skip during conversion
        **options: Backend-specific options

    Returns:
        An HTML to Markdown converter

    Raises:
        ImportError: If the requested backend is not available
        ValueError: If no suitable backend is available
    """
    return HtmlToMarkdownFactory.create(
        backend,
        heading_style=heading_style,
        link_style=link_style,
        code_block_style=code_block_style,
        code_fence_style=code_fence_style,
        list_marker_style=list_marker_style,
        line_break_style=line_break_style,
        hr_style=hr_style,
        emphasis_style=emphasis_style,
        skip_tags=skip_tags,
        **options,
    )
