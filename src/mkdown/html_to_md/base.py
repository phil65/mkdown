"""Base classes for HTML to Markdown converters."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, ClassVar, Literal


HeadingStyle = Literal["atx", "setext", "atx_closed"]
LinkStyle = Literal["inline", "reference"]
CodeBlockStyle = Literal["indented", "fenced"]
CodeFenceStyle = Literal["backticks", "tildes"]
ListMarkerStyle = Literal["asterisk", "dash", "plus"]
LineBreakStyle = Literal["spaces", "backslash"]
HorizontalRuleStyle = Literal["dashes", "asterisks", "underscores"]
EmphasisStyle = Literal["asterisk", "underscore"]


class BaseHtmlToMarkdown(ABC):
    """Base class for HTML to Markdown converters with common options."""

    # Default values
    DEFAULT_HEADING_STYLE: ClassVar[HeadingStyle] = "atx"
    DEFAULT_LINK_STYLE: ClassVar[LinkStyle] = "inline"
    DEFAULT_CODE_BLOCK_STYLE: ClassVar[CodeBlockStyle] = "fenced"
    DEFAULT_CODE_FENCE_STYLE: ClassVar[CodeFenceStyle] = "backticks"
    DEFAULT_LIST_MARKER_STYLE: ClassVar[ListMarkerStyle] = "asterisk"
    DEFAULT_LINE_BREAK_STYLE: ClassVar[LineBreakStyle] = "spaces"
    DEFAULT_HR_STYLE: ClassVar[HorizontalRuleStyle] = "asterisks"
    DEFAULT_EMPHASIS_STYLE: ClassVar[EmphasisStyle] = "asterisk"

    def __init__(
        self,
        # Common options shared across implementations
        heading_style: HeadingStyle | None = None,
        link_style: LinkStyle | None = None,
        code_block_style: CodeBlockStyle | None = None,
        code_fence_style: CodeFenceStyle | None = None,
        list_marker_style: ListMarkerStyle | None = None,
        line_break_style: LineBreakStyle | None = None,
        hr_style: HorizontalRuleStyle | None = None,
        emphasis_style: EmphasisStyle | None = None,
        # HTML tags handling
        skip_tags: list[str] | None = None,
        # Implementation-specific options
        **options: Any,
    ) -> None:
        """Initialize HTML to Markdown converter with common options.

        Args:
            heading_style: Style for headings
            link_style: Style for links
            code_block_style: Style for code blocks
            code_fence_style: Style for code fences
            list_marker_style: Style for bullet list markers
            line_break_style: Style for line breaks
            hr_style: Style for horizontal rules
            emphasis_style: Style for emphasis
            skip_tags: HTML tags to skip during conversion
            **options: Additional implementation-specific options
        """
        self._heading_style = heading_style or self.DEFAULT_HEADING_STYLE
        self._link_style = link_style or self.DEFAULT_LINK_STYLE
        self._code_block_style = code_block_style or self.DEFAULT_CODE_BLOCK_STYLE
        self._code_fence_style = code_fence_style or self.DEFAULT_CODE_FENCE_STYLE
        self._list_marker_style = list_marker_style or self.DEFAULT_LIST_MARKER_STYLE
        self._line_break_style = line_break_style or self.DEFAULT_LINE_BREAK_STYLE
        self._hr_style = hr_style or self.DEFAULT_HR_STYLE
        self._emphasis_style = emphasis_style or self.DEFAULT_EMPHASIS_STYLE
        self._skip_tags = skip_tags
        self._additional_options = options

        # Initialize implementation-specific options
        self._initialize_options()

    @abstractmethod
    def _initialize_options(self) -> None:
        """Initialize implementation-specific options.

        This method should be overridden by subclasses to set up
        their implementation-specific options based on the common options
        and any additional options provided.
        """
        ...

    @abstractmethod
    def convert(self, html: str) -> str:
        """Convert HTML to Markdown.

        Args:
            html: HTML content to convert

        Returns:
            Markdown representation of the HTML
        """
        ...
