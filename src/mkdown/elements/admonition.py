from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from html import escape
from typing import Any, ClassVar


ICON_MAP = {
    "note": "📝",
    "warning": "⚠️",
    "danger": "🚨",
    "tip": "💡",
    "info": "ℹ️",  # noqa: RUF001
    "caution": "⚠️",
    "important": "❗",
    "success": "✅",
}

ROLE_MAP = {
    "note": "note",
    "warning": "alert",
    "danger": "alert",
    "tip": "note",
    "info": "note",
    "caution": "alert",
    "important": "alert",
    "success": "status",
}


class AdmonitionType(Enum):
    NOTE = "note"
    WARNING = "warning"
    DANGER = "danger"
    TIP = "tip"
    INFO = "info"
    CAUTION = "caution"
    IMPORTANT = "important"
    SUCCESS = "success"

    @property
    def default_icon(self) -> str:
        return ICON_MAP.get(self.value, "ℹ️")  # noqa: RUF001

    @property
    def default_aria_role(self) -> str:
        return ROLE_MAP.get(self.value, "note")


class CustomAdmonitionType:
    def __init__(
        self,
        name: str,
        icon: str | None = None,
        aria_role: str = "note",
        css_class: str | None = None,
        color: str | None = None,
    ):
        self.name = name
        self.value = name.lower()
        self.icon = icon
        self.aria_role = aria_role
        self.css_class = css_class or self.value
        self.color = color

    def __eq__(self, other):
        if isinstance(other, CustomAdmonitionType):
            return self.value == other.value
        return False


class MarkdownFlavor(Enum):
    SPHINX = "sphinx"
    MKDOCS = "mkdocs"
    DOCUSAURUS = "docusaurus"
    GITHUB = "github"
    GITLAB = "gitlab"
    COMMONMARK = "commonmark"
    HTML = "html"


@dataclass
class ThemeSupport:
    name: str
    css_framework: str
    css_classes: dict[str, str]
    custom_icons: dict[str, str]
    custom_colors: dict[str, str]
    supports_dark_mode: bool = False
    rtl_support: bool = False


@dataclass
class AdmonitionMetadata:
    """Metadata for admonition support in different flavors."""

    required_extensions: set[str]
    supported_types: set[AdmonitionType]
    allows_custom_types: bool
    allows_custom_titles: bool
    allows_collapsible: bool
    allows_nesting: bool
    syntax_type: str  # "directive", "block", "html"
    css_classes: list[str] = field(default_factory=list)
    icon_support: bool = False
    default_css_framework: str | None = None
    supported_themes: dict[str, ThemeSupport] = field(default_factory=dict)
    accessibility_features: set[str] = field(default_factory=set)
    custom_types: dict[str, CustomAdmonitionType] = field(default_factory=dict)
    max_nesting_level: int = 1


class AdmonitionFormatter:
    """Base class for formatting admonitions."""

    def format(
        self,
        admonition: Admonition,
        strict: bool = False,
        theme: str | None = None,
        **kwargs: Any,
    ) -> str:
        raise NotImplementedError

    def _get_effective_title(
        self, admonition: Admonition, metadata: AdmonitionMetadata
    ) -> str:
        if metadata.allows_custom_titles:
            return admonition.title
        return admonition.admonition_type.value.title()

    def _process_nested_content(
        self, content: str, level: int, metadata: AdmonitionMetadata
    ) -> str:
        if level > metadata.max_nesting_level:
            return content
        # Process nested admonitions in content
        # This would need to parse the content and handle nested admonitions
        return content


class HTMLFormatter(AdmonitionFormatter):
    def format(
        self,
        admonition: Admonition,
        strict: bool = False,
        theme: str | None = None,
        **kwargs: Any,
    ) -> str:
        metadata = AdmonitionSupport.METADATA[MarkdownFlavor.HTML]
        theme_support = metadata.supported_themes.get(theme) if theme else None

        css_class = f"admonition {admonition.admonition_type.value}"
        if admonition.custom_class:
            css_class += f" {admonition.custom_class}"
        if theme_support:
            css_class += (
                f" {theme_support.css_classes.get(admonition.admonition_type.value, '')}"
            )

        icon_html = ""
        if admonition.icon and metadata.icon_support:
            theme_icon = (
                theme_support.custom_icons.get(admonition.admonition_type.value)
                if theme_support
                else None
            )
            icon = theme_icon or admonition.icon
            icon_html = (
                f'<span class="admonition-icon" aria-hidden="true">{escape(icon)}</span>'
            )

        collapse_attrs = ' class="collapse"' if admonition.collapse else ""

        # Add accessibility attributes
        aria_role = (
            admonition.admonition_type.default_aria_role
            if isinstance(admonition.admonition_type, AdmonitionType)
            else "note"
        )

        return f"""
<div class="{css_class}" role="{aria_role}">
    <div class="admonition-title"{collapse_attrs}>
        {icon_html}
        <span class="admonition-title-text">{escape(admonition.title)}</span>
    </div>
    <div class="admonition-content">
        {admonition._process_nested_content(escape(admonition.content))}
    </div>
</div>
""".strip()


class AdmonitionSupport:
    """Registry of markdown flavor support for admonitions."""

    FORMATTERS: ClassVar[dict[MarkdownFlavor, AdmonitionFormatter]] = {}

    # Define common themes and their support
    MATERIAL_THEME = ThemeSupport(
        name="material",
        css_framework="material",
        css_classes={
            "note": "md-note",
            "warning": "md-warning",
            # ... other type classes
        },
        custom_icons={
            "note": "<svg>...</svg>",  # Material Design icons
            "warning": "<svg>...</svg>",
            # ... other icons
        },
        custom_colors={
            "note": "#448aff",
            "warning": "#ff9100",
            # ... other colors
        },
        supports_dark_mode=True,
        rtl_support=True,
    )

    SPHINX_THEME = ThemeSupport(
        name="sphinx_rtd",
        css_framework="sphinx",
        css_classes={
            "note": "sphinx-note",
            "warning": "sphinx-warning",
            # ... other classes
        },
        custom_icons={},  # Sphinx doesn't use icons by default
        custom_colors={},
        supports_dark_mode=False,
        rtl_support=True,
    )

    METADATA: ClassVar = {
        MarkdownFlavor.SPHINX: AdmonitionMetadata(
            required_extensions=set(),
            supported_types=set(AdmonitionType),
            allows_custom_types=True,
            allows_custom_titles=True,
            allows_collapsible=False,
            allows_nesting=True,
            syntax_type="directive",
            accessibility_features={"aria-roles", "semantic-markup"},
            supported_themes={
                "sphinx_rtd": SPHINX_THEME,
                # ... other Sphinx themes
            },
            max_nesting_level=2,
        ),
        MarkdownFlavor.MKDOCS: AdmonitionMetadata(
            required_extensions={"admonition", "pymdownx.details"},
            supported_types=set(AdmonitionType),
            allows_custom_types=True,
            allows_custom_titles=True,
            allows_collapsible=True,
            allows_nesting=True,
            syntax_type="block",
            icon_support=True,
            accessibility_features={"aria-roles", "semantic-markup", "color-contrast"},
            supported_themes={
                "material": MATERIAL_THEME,
                # ... other MkDocs themes
            },
            max_nesting_level=3,
        ),
        # ... other flavors
    }

    @classmethod
    def initialize_formatters(cls):
        """Initialize formatters if not already done."""
        if not cls.FORMATTERS:
            cls.FORMATTERS[MarkdownFlavor.HTML] = HTMLFormatter()
            cls.FORMATTERS[MarkdownFlavor.COMMONMARK] = HTMLFormatter()  # Fallback

    @classmethod
    def register_custom_type(
        cls, custom_type: CustomAdmonitionType, flavor: MarkdownFlavor
    ) -> None:
        """Register a custom admonition type for a specific flavor."""
        metadata = cls.METADATA.get(flavor)
        if metadata and metadata.allows_custom_types:
            metadata.custom_types[custom_type.value] = custom_type

    @classmethod
    def get_css(
        cls, framework: str = "custom", theme: str | None = None, dark_mode: bool = False
    ) -> str:
        """Return CSS for styling admonitions."""
        if framework == "custom":
            dark_mode_css = (
                """
            @media (prefers-color-scheme: dark) {
                .admonition { background: #1a1a1a; }
                .admonition.note { border-color: #448aff; background: #1a1f2f; }
                /* ... other dark mode styles ... */
            }
            """
                if dark_mode
                else ""
            )

            return f"""
            .admonition {{
                margin: 1em 0;
                padding: 0.1em 1em;
                border-left: 4px solid;
                border-radius: 4px;
                transition: all 0.3s ease;
            }}
            .admonition-title {{
                font-weight: bold;
                margin: 0.5em 0;
                display: flex;
                align-items: center;
                gap: 0.5em;
            }}
            .admonition-icon {{
                display: inline-flex;
                align-items: center;
            }}
            .admonition.note {{ border-color: #448aff; background: #f1f8ff; }}
            .admonition.warning {{ border-color: #ff9100; background: #fff8f0; }}
            .admonition.danger {{ border-color: #ff1744; background: #fff1f0; }}
            /* Nested admonition styles */
            .admonition .admonition {{
                margin-left: 1em;
                margin-right: 1em;
            }}
            /* Collapse styles */
            .admonition-title.collapse + .admonition-content {{
                display: none;
            }}
            .admonition-title.collapse.active + .admonition-content {{
                display: block;
            }}
            {dark_mode_css}
            """.strip()
        return ""  # Add other framework CSS as needed


class Admonition:
    def __init__(
        self,
        content: str,
        admonition_type: AdmonitionType | CustomAdmonitionType,
        title: str | None = None,
        collapse: bool = False,
        icon: str | None = None,
        custom_class: str | None = None,
        nesting_level: int = 0,
    ):
        self.content = content
        self.admonition_type = admonition_type
        self.title = title or (
            admonition_type.value.title()
            if isinstance(admonition_type, AdmonitionType)
            else admonition_type.name
        )
        self.collapse = collapse
        self.icon = icon or (
            admonition_type.default_icon
            if isinstance(admonition_type, AdmonitionType)
            else admonition_type.icon
        )
        self.custom_class = custom_class
        self.nesting_level = nesting_level

    def to_markdown(
        self,
        flavor: MarkdownFlavor,
        strict: bool = False,
        theme: str | None = None,
        **kwargs: Any,
    ) -> str:
        metadata = AdmonitionSupport.METADATA.get(flavor)
        if not metadata:
            if strict:
                msg = f"Unsupported markdown flavor: {flavor}"
                raise ValueError(msg)
            return self.to_markdown(MarkdownFlavor.COMMONMARK)

        # Validation in strict mode
        if strict:
            if (
                isinstance(self.admonition_type, AdmonitionType)
                and self.admonition_type not in metadata.supported_types
            ):
                msg = f"Admonition type {self.admonition_type} not supported in {flavor}"
                raise ValueError(msg)
            if self.collapse and not metadata.allows_collapsible:
                msg = f"Collapsible admonitions not supported in {flavor}"
                raise ValueError(msg)
            if self.icon and not metadata.icon_support:
                msg = f"Icons not supported in {flavor}"
                raise ValueError(msg)
            if self.nesting_level > metadata.max_nesting_level:
                lvl = metadata.max_nesting_level
                msg = f"Nesting level {self.nesting_level} exceeds maximum of {lvl}"
                raise ValueError(msg)

        formatter = AdmonitionSupport.FORMATTERS.get(flavor)
        if not formatter:
            if strict:
                msg = f"No formatter available for {flavor}"
                raise ValueError(msg)
            return self.to_markdown(MarkdownFlavor.COMMONMARK)

        return formatter.format(self, strict=strict, theme=theme, **kwargs)

    def to_html(
        self,
        theme: str | None = None,
        css_framework: str | None = None,
        **kwargs: Any,
    ) -> str:
        """Convert admonition to HTML with optional theme and CSS framework."""
        return self.to_markdown(
            MarkdownFlavor.HTML, theme=theme, css_framework=css_framework, **kwargs
        )

    def _indent_content(self, content: str, spaces: int = 4) -> str:
        return "\n".join(f"{' ' * spaces}{line}" for line in content.split("\n"))

    def _process_nested_content(self, content: str) -> str:
        """Process content for nested admonitions."""
        if self.nesting_level > 0:
            # Process nested admonition content
            pass
        return content


if __name__ == "__main__":
    # Create a custom admonition type
    custom_type = CustomAdmonitionType(
        name="Example",
        icon="🔍",
        aria_role="note",
        css_class="custom-example",
        color="#7c4dff",
    )

    # Register the custom type
    AdmonitionSupport.register_custom_type(custom_type, MarkdownFlavor.MKDOCS)

    # Create an admonition with the custom type
    admonition = Admonition(
        content="This is a custom admonition", admonition_type=custom_type, collapse=True
    )

    # Convert to HTML with theme support
    html = admonition.to_html(theme="material", dark_mode=True, strict=False)

    # Get theme-specific CSS
    css = AdmonitionSupport.get_css(
        framework="material", theme="material", dark_mode=True
    )
