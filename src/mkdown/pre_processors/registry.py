"""Registry for pre processors."""

from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from mkdown.pre_processors.base import PreProcessor


class PreProcessorRegistry:
    """Registry for pre processors."""

    def __init__(self) -> None:
        """Initialize empty processor collection."""
        self._processors: list[PreProcessor] = []
        self._sorted = True

    def register_processor(self, processor: PreProcessor) -> None:
        """Register a pre processor.

        Args:
            processor: The processor to register
        """
        self._processors.append(processor)
        self._sorted = False

    def _ensure_sorted(self) -> None:
        """Sort processors by priority if needed."""
        if not self._sorted:
            self._processors.sort(key=lambda x: -x.priority)
            self._sorted = True

    @property
    def processors(self) -> list[PreProcessor]:
        """Get sorted pre processors."""
        self._ensure_sorted()
        return self._processors

    @property
    def has_processors(self) -> bool:
        """Check if there are any pre processors."""
        return bool(self._processors)
