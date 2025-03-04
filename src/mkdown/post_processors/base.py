"""Base classes for post processors that transform HTML text."""

from __future__ import annotations

from abc import ABC, abstractmethod


class PostProcessor(ABC):
    """Abstract base class for post processors that transform HTML text."""

    def __init__(self, priority: int = 100) -> None:
        """Initialize with a priority.

        Args:
            priority: Execution priority (higher runs earlier)
        """
        self._priority = priority

    @abstractmethod
    def process_html(self, html: str) -> str:
        """Process and potentially transform HTML text.

        Args:
            html: The HTML text to process

        Returns:
            The processed HTML text
        """
        ...

    @property
    def priority(self) -> int:
        """The priority of this processor (higher runs earlier)."""
        return self._priority

    @priority.setter
    def priority(self, value: int) -> None:
        """Set the priority of this processor."""
        self._priority = value
