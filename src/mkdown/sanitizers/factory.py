"""Factory for creating HTML sanitizers."""

from __future__ import annotations

import importlib.util
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from collections.abc import Sequence

    from mkdown.sanitizers.base import HTMLSanitizer


# Check for sanitizer availability once at module import
NH3_AVAILABLE = importlib.util.find_spec("nh3") is not None
BLEACH_AVAILABLE = importlib.util.find_spec("bleach") is not None


def create_sanitizer(
    tags: Sequence[str] | None = None,
    attributes: dict[str, set[str]] | None = None,
    protocols: Sequence[str] | None = None,
    strip_comments: bool = True,
    sanitizer_name: str | None = None,
    **kwargs,
) -> HTMLSanitizer:
    """Create the best available HTML sanitizer.

    Args:
        tags: HTML tags to allow (None for default)
        attributes: HTML attributes to allow (None for default)
        protocols: URL protocols to allow (None for default)
        strip_comments: Whether to strip HTML comments
        sanitizer_name: Optional name of sanitizer to use ('nh3' or 'bleach')
        **kwargs: Additional sanitizer-specific options

    Returns:
        An instance of the requested or best available sanitizer

    Raises:
        ImportError: If no sanitizer is available
    """
    # Try to use the specified sanitizer
    tags_ = set(tags) if tags else None
    protocols_ = set(protocols) if protocols else None
    if sanitizer_name == "nh3" and NH3_AVAILABLE:
        from mkdown.sanitizers.nh3_sanitizer import NH3Sanitizer

        return NH3Sanitizer(
            tags=tags_,
            attributes=attributes,
            protocols=protocols_,
            strip_comments=strip_comments,
            **kwargs,
        )

    if sanitizer_name == "bleach" and BLEACH_AVAILABLE:
        from mkdown.sanitizers.bleach_sanitizer import BleachSanitizer

        return BleachSanitizer(
            tags=tags_,
            attributes=attributes,
            protocols=protocols_,
            strip_comments=strip_comments,
            **kwargs,
        )

    # Auto-select the best available sanitizer
    if NH3_AVAILABLE:
        from mkdown.sanitizers.nh3_sanitizer import NH3Sanitizer

        return NH3Sanitizer(
            tags=tags_,
            attributes=attributes,
            protocols=protocols_,
            strip_comments=strip_comments,
            **kwargs,
        )

    if BLEACH_AVAILABLE:
        from mkdown.sanitizers.bleach_sanitizer import BleachSanitizer

        return BleachSanitizer(
            tags=tags_,
            attributes=attributes,
            protocols=protocols_,
            strip_comments=strip_comments,
            **kwargs,
        )

    msg = (
        "No HTML sanitizer available. Install one of: "
        "'nh3' (recommended, Rust-based) or 'bleach' (pure Python)."
    )
    raise ImportError(msg)
