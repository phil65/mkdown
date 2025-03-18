"""HTML to Markdown converter implementation using markdownify."""

from __future__ import annotations

from dataclasses import dataclass, field
import importlib.util
from typing import TYPE_CHECKING, Any, ClassVar

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


if TYPE_CHECKING:
    from collections.abc import Callable


# Check if markdownify is available
MARKDOWNIFY_AVAILABLE = importlib.util.find_spec("markdownify") is not None


def _map_heading_style(style: HeadingStyle) -> str:
    """Map our heading style to markdownify's heading style.

    Args:
        style: Our heading style

    Returns:
        Markdownify's heading style
    """
    if style == "atx":
        return "ATX"
    if style == "atx_closed":
        return "ATX_CLOSED"
    return "SETEXT"


def _map_emphasis_style(style: EmphasisStyle) -> str:
    """Map our emphasis style to markdownify's emphasis style.

    Args:
        style: Our emphasis style

    Returns:
        Markdownify's emphasis style
    """
    if style == "asterisk":
        return "ASTERISK"
    return "UNDERSCORE"


def _map_newline_style(style: LineBreakStyle) -> str:
    """Map our line break style to markdownify's newline style.

    Args:
        style: Our line break style

    Returns:
        Markdownify's newline style
    """
    if style == "spaces":
        return "SPACES"
    return "BACKSLASH"


def _map_list_marker_to_bullets(style: ListMarkerStyle) -> str:
    """Map list marker style to markdownify bullets string.

    Args:
        style: List marker style

    Returns:
        Markdownify bullets string
    """
    if style == "asterisk":
        return "*"
    if style == "dash":
        return "-"
    if style == "plus":
        return "+"
    return "*+-"


@dataclass
class MarkdownifyOptions:
    """Options for the markdownify converter."""

    # Common options
    heading_style: HeadingStyle = "atx"
    bullets: str = "*"
    strong_em_symbol: EmphasisStyle = "asterisk"
    newline_style: LineBreakStyle = "spaces"
    strip: list[str] | None = None

    # Markdownify-specific options
    convert: list[str] | None = None
    autolinks: bool = True
    default_title: bool = False
    sub_symbol: str = ""
    sup_symbol: str = ""
    code_language: str = ""
    code_language_callback: Callable | None = None
    escape_asterisks: bool = True
    escape_underscores: bool = True
    escape_misc: bool = False
    keep_inline_images_in: list[str] = field(default_factory=list)
    table_infer_header: bool = False
    wrap: bool = False
    wrap_width: int | None = 80
    strip_document: str | None = "STRIP"


class MarkdownifyConverter(BaseHtmlToMarkdown):
    """HTML to Markdown converter using markdownify."""

    REQUIRED_PACKAGES: ClassVar = {"markdownify"}

    def __init__(
        self,
        # Common options from BaseHtmlToMarkdown
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
    ) -> None:
        """Initialize markdownify converter with options.

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
            **options: Additional options

        Raises:
            ImportError: If markdownify is not installed
        """
        if not MARKDOWNIFY_AVAILABLE:
            msg = (
                "markdownify is not installed. Install it with 'pip install markdownify'."
            )
            raise ImportError(msg)

        # Store markdownify-specific options
        self._convert = convert
        self._autolinks = autolinks
        self._default_title = default_title
        self._sub_symbol = sub_symbol
        self._sup_symbol = sup_symbol
        self._code_language = code_language
        self._code_language_callback = code_language_callback
        self._escape_asterisks = escape_asterisks
        self._escape_underscores = escape_underscores
        self._escape_misc = escape_misc
        self._keep_inline_images_in = keep_inline_images_in or []
        self._table_infer_header = table_infer_header
        self._wrap = wrap
        self._wrap_width = wrap_width
        self._strip_document = strip_document

        # Call parent constructor
        super().__init__(
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

    def _initialize_options(self) -> None:
        """Initialize markdownify-specific options."""
        self._options = MarkdownifyOptions(
            # Common options
            heading_style=self._heading_style,  # pyright: ignore
            bullets=_map_list_marker_to_bullets(self._list_marker_style),  # pyright: ignore
            strong_em_symbol=self._emphasis_style,  # pyright: ignore
            newline_style=self._line_break_style,  # pyright: ignore
            strip=self._skip_tags,
            # Markdownify-specific options
            convert=self._convert,
            autolinks=self._autolinks,
            default_title=self._default_title,
            sub_symbol=self._sub_symbol,
            sup_symbol=self._sup_symbol,
            code_language=self._code_language,
            code_language_callback=self._code_language_callback,
            escape_asterisks=self._escape_asterisks,
            escape_underscores=self._escape_underscores,
            escape_misc=self._escape_misc,
            keep_inline_images_in=self._keep_inline_images_in,
            table_infer_header=self._table_infer_header,
            wrap=self._wrap,
            wrap_width=self._wrap_width,
            strip_document=self._strip_document,
        )

    def convert(self, html: str) -> str:
        """Convert HTML to Markdown using markdownify.

        Args:
            html: HTML content to convert

        Returns:
            Markdown representation of the HTML
        """
        from markdownify import markdownify

        # Convert using markdownify with directly passed options
        return markdownify(
            html,
            heading_style=_map_heading_style(self._options.heading_style),
            bullets=self._options.bullets,
            strong_em_symbol=_map_emphasis_style(self._options.strong_em_symbol),
            newline_style=_map_newline_style(self._options.newline_style),
            strip=self._options.strip,
            convert=self._options.convert,
            autolinks=self._options.autolinks,
            default_title=self._options.default_title,
            sub_symbol=self._options.sub_symbol,
            sup_symbol=self._options.sup_symbol,
            code_language=self._options.code_language,
            code_language_callback=self._options.code_language_callback,
            escape_asterisks=self._options.escape_asterisks,
            escape_underscores=self._options.escape_underscores,
            escape_misc=self._options.escape_misc,
            keep_inline_images_in=self._options.keep_inline_images_in,
            table_infer_header=self._options.table_infer_header,
            wrap=self._options.wrap,
            wrap_width=self._options.wrap_width,
            strip_document=self._options.strip_document,
        )

    def with_options(self, **options: Any) -> MarkdownifyConverter:
        """Create a new converter with updated options.

        Args:
            **options: Options to update

        Returns:
            A new converter instance with the updated options
        """
        # Create new options, starting with current values for common options
        heading_style = options.get("heading_style", self._heading_style)
        link_style = options.get("link_style", self._link_style)
        code_block_style = options.get("code_block_style", self._code_block_style)
        code_fence_style = options.get("code_fence_style", self._code_fence_style)
        list_marker_style = options.get("list_marker_style", self._list_marker_style)
        line_break_style = options.get("line_break_style", self._line_break_style)
        hr_style = options.get("hr_style", self._hr_style)
        emphasis_style = options.get("emphasis_style", self._emphasis_style)
        skip_tags = options.get("skip_tags", self._skip_tags)

        # Create new options, starting with current values for markdownify-specific opts
        convert = options.get("convert", self._convert)
        autolinks = options.get("autolinks", self._autolinks)
        default_title = options.get("default_title", self._default_title)
        sub_symbol = options.get("sub_symbol", self._sub_symbol)
        sup_symbol = options.get("sup_symbol", self._sup_symbol)
        code_language = options.get("code_language", self._code_language)
        code_language_callback = options.get(
            "code_language_callback", self._code_language_callback
        )
        escape_asterisks = options.get("escape_asterisks", self._escape_asterisks)
        escape_underscores = options.get("escape_underscores", self._escape_underscores)
        escape_misc = options.get("escape_misc", self._escape_misc)
        keep_inline_images_in = options.get(
            "keep_inline_images_in", self._keep_inline_images_in
        )
        table_infer_header = options.get("table_infer_header", self._table_infer_header)
        wrap = options.get("wrap", self._wrap)
        wrap_width = options.get("wrap_width", self._wrap_width)
        strip_document = options.get("strip_document", self._strip_document)

        # Get any additional options
        additional_options = {
            k: v
            for k, v in options.items()
            if k
            not in {
                "heading_style",
                "link_style",
                "code_block_style",
                "code_fence_style",
                "list_marker_style",
                "line_break_style",
                "hr_style",
                "emphasis_style",
                "skip_tags",
                "convert",
                "autolinks",
                "default_title",
                "sub_symbol",
                "sup_symbol",
                "code_language",
                "code_language_callback",
                "escape_asterisks",
                "escape_underscores",
                "escape_misc",
                "keep_inline_images_in",
                "table_infer_header",
                "wrap",
                "wrap_width",
                "strip_document",
            }
        }

        # Create new converter with explicit arguments
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
            **additional_options,
        )
