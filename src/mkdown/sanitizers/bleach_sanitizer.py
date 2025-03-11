"""HTML sanitization using bleach."""

from __future__ import annotations

import importlib.util

from mkdown.sanitizers.base import HTMLSanitizer


# Check for bleach availability
BLEACH_AVAILABLE = importlib.util.find_spec("bleach") is not None


class BleachSanitizer(HTMLSanitizer):
    """HTML sanitizer implementation using bleach."""

    def __init__(
        self,
        tags: set[str] | None = None,
        attributes: dict[str, set[str]] | None = None,
        protocols: set[str] | None = None,
        strip_comments: bool = True,
        strip: bool = True,
    ) -> None:
        """Initialize the Bleach sanitizer.

        Args:
            tags: HTML tags to allow (None for default)
            attributes: HTML attributes to allow (None for default)
            protocols: URL protocols to allow (None for default)
            strip_comments: Whether to strip comments
            strip: Whether to strip disallowed tags

        Raises:
            ImportError: If bleach is not installed
        """
        super().__init__(tags, attributes, protocols, strip_comments)

        if not BLEACH_AVAILABLE:
            msg = "Bleach sanitizer requires 'bleach' package."
            raise ImportError(msg)

        self.strip = strip

    def sanitize(self, html: str) -> str:
        """Sanitize HTML using bleach.

        Args:
            html: HTML content to sanitize

        Returns:
            Sanitized HTML
        """
        import bleach

        attributes = self.attributes or {}
        return bleach.clean(
            html,
            tags=self.tags or [],
            attributes={k: list(v) for k, v in attributes.items()},
            protocols=self.protocols or [],
            strip=self.strip,
            strip_comments=self.strip_comments,
        )
