"""Python-Markdown parser implementation."""

from __future__ import annotations

from typing import Any


def markdown_to_html(
    markdown_text: str,
    *,
    # Common options that match our interface
    strikethrough: bool = False,
    table: bool = False,
    autolink: bool = False,
    tasklist: bool = False,
    math: bool = False,
    unsafe_: bool = False,
    # Additional options specific to python-markdown
    extensions: list[str] | None = None,
    extension_configs: dict[str, dict[str, Any]] | None = None,
    output_format: str = "html",
    **kwargs: Any,
) -> str:
    """Convert markdown to HTML using the Python-Markdown library.

    Args:
        markdown_text: Input markdown text
        strikethrough: Enable strikethrough extension
        table: Enable tables extension
        autolink: Enable linkify extension
        tasklist: Enable task lists
        math: Enable math extension
        unsafe_: Allow raw HTML
        extensions: Additional Python-Markdown extensions
        extension_configs: Configuration for extensions
        output_format: Output format (html, html5, xhtml, etc.)
        kwargs: Additional keyword arguments passed to Python-Markdown

    Returns:
        HTML output as string
    """
    import markdown

    # Initialize extensions list
    md_extensions = extensions.copy() if extensions else []

    # Map common options to python-markdown extensions
    if strikethrough:
        md_extensions.append("pymdownx.tilde")
    if table:
        md_extensions.append("tables")
    if autolink:
        md_extensions.append("pymdownx.magiclink")
    if tasklist:
        md_extensions.append("pymdownx.tasklist")
    if math:
        md_extensions.append("pymdownx.arithmatex")

    # Set up extension configs
    configs = extension_configs.copy() if extension_configs else {}

    # Apply unsafe option
    if unsafe_:
        # Allow raw HTML if unsafe is enabled
        kwargs["safe_mode"] = False
    else:
        # Otherwise, apply safe mode
        kwargs["safe_mode"] = True

    # Convert to HTML
    return markdown.markdown(
        markdown_text,
        extensions=md_extensions,
        extension_configs=configs,
        output_format=output_format,
        **kwargs,
    )
