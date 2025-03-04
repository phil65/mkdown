"""Base class for pre processors that transform markdown text before parsing."""

from __future__ import annotations

from abc import ABC, abstractmethod


class PreProcessor(ABC):
    """ABC for pre processors that transform markdown text before parsing."""

    def __init__(self, priority: int = 100) -> None:
        """Initialize with a priority.

        Args:
            priority: Execution priority (higher runs earlier)
        """
        self._priority = priority

    @abstractmethod
    def process_markdown(self, markdown: str) -> str:
        """Process and potentially transform markdown text before parsing.

        Args:
            markdown: The markdown text to process

        Returns:
            The processed markdown text
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
