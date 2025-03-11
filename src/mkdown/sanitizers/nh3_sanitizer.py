"""HTML sanitization using nh3 (Rust-based)."""

from __future__ import annotations

import importlib.util

from mkdown.sanitizers.base import HTMLSanitizer


# Check for nh3 availability
NH3_AVAILABLE = importlib.util.find_spec("nh3") is not None


class NH3Sanitizer(HTMLSanitizer):
    """HTML sanitizer implementation using nh3 (Rust-based)."""

    def __init__(
        self,
        tags: set[str] | None = None,
        attributes: dict[str, set[str]] | None = None,
        protocols: set[str] | None = None,
        strip_comments: bool = True,
        link_rel: str | None = "noopener noreferrer",
    ) -> None:
        """Initialize the NH3 sanitizer.

        Args:
            tags: HTML tags to allow (None for default)
            attributes: HTML attributes to allow (None for default)
            protocols: URL protocols to allow (None for default)
            strip_comments: Whether to strip comments
            link_rel: rel attribute for links

        Raises:
            ImportError: If nh3 is not installed
        """
        super().__init__(tags, attributes, protocols, strip_comments)

        if not NH3_AVAILABLE:
            msg = "NH3 sanitizer requires 'nh3' package."
            raise ImportError(msg)

        self.link_rel = link_rel

    def sanitize(self, html: str) -> str:
        """Sanitize HTML using nh3.

        Args:
            html: HTML content to sanitize

        Returns:
            Sanitized HTML
        """
        import nh3

        return nh3.clean(
            html,
            tags=self.tags,
            attributes=self.attributes,
            url_schemes=self.protocols,
            strip_comments=self.strip_comments,
            link_rel=self.link_rel,
        )
