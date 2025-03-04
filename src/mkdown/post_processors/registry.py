"""Post processor registry."""

from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from mkdown.post_processors.sanitizer import PostProcessor


class PostProcessorRegistry:
    """Registry for post processors."""

    def __init__(self) -> None:
        """Initialize empty processor collection."""
        self._processors: list[PostProcessor] = []
        self._sorted = True

    def register_processor(self, processor: PostProcessor) -> None:
        """Register a post processor.

        Args:
            processor: The processor to register
        """
        self._processors.append(processor)
        self._sorted = False

    def _ensure_sorted(self) -> None:
        """Sort processors by priority if needed."""
        if not self._sorted:
            self._processors.sort(key=lambda x: -x.priority)  # Higher priority first
            self._sorted = True

    @property
    def processors(self) -> list[PostProcessor]:
        """Get sorted post processors."""
        self._ensure_sorted()
        return self._processors

    @property
    def has_processors(self) -> bool:
        """Check if there are any post processors."""
        return bool(self._processors)
