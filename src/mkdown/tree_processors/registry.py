"""Registry for tree processors."""

from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from mkdown.tree_processors.base import ETTreeProcessor, LXMLTreeProcessor


class TreeProcessorRegistry:
    """Registry for tree processors with separate ET and LXML collections."""

    def __init__(self) -> None:
        """Initialize empty processor collections."""
        self._et_processors: list[ETTreeProcessor] = []
        self._lxml_processors: list[LXMLTreeProcessor] = []
        self._sorted = True

    def register_et_processor(self, processor: ETTreeProcessor) -> None:
        """Register an ElementTree processor.

        Args:
            processor: The processor to register
        """
        self._et_processors.append(processor)
        self._sorted = False

    def register_lxml_processor(self, processor: LXMLTreeProcessor) -> None:
        """Register an lxml processor.

        Args:
            processor: The processor to register
        """
        self._lxml_processors.append(processor)
        self._sorted = False

    def _ensure_sorted(self) -> None:
        """Sort processors by priority if needed."""
        if not self._sorted:
            self._et_processors.sort(key=lambda x: -x.priority)  # Higher priority first
            self._lxml_processors.sort(key=lambda x: -x.priority)
            self._sorted = True

    @property
    def et_processors(self) -> list[ETTreeProcessor]:
        """Get sorted ElementTree processors."""
        self._ensure_sorted()
        return self._et_processors

    @property
    def lxml_processors(self) -> list[LXMLTreeProcessor]:
        """Get sorted lxml processors."""
        self._ensure_sorted()
        return self._lxml_processors

    @property
    def has_et_processors(self) -> bool:
        """Check if there are any ElementTree processors."""
        return bool(self._et_processors)

    @property
    def has_lxml_processors(self) -> bool:
        """Check if there are any lxml processors."""
        return bool(self._lxml_processors)
