"""Module for custom markdown fence handling with pymdownx.superfences."""

from __future__ import annotations

from collections import UserDict
from dataclasses import dataclass
import functools
from typing import TYPE_CHECKING, Any, ClassVar, Protocol


if TYPE_CHECKING:
    from collections.abc import Callable, Iterator


class FenceFormatter(Protocol):
    """Protocol for fence formatters."""

    def __call__(self, content: str, options: dict[str, Any]) -> str: ...


@dataclass
class CustomFence:
    """Represents a custom fence configuration."""

    name: str
    formatter: FenceFormatter
    description: str = ""

    def to_superfences_format(self) -> dict[str, Any]:
        """Convert to superfences custom fence format."""
        return {
            "name": self.name,
            "class": "",
            "format": self._adapt_formatter(self.formatter),
        }

    @staticmethod
    def _adapt_formatter(formatter: FenceFormatter) -> Callable[..., str]:
        """Adapt our formatter interface to superfences interface."""

        @functools.wraps(formatter)
        def wrapper(
            source: str,
            language: str,
            css_class: str | None = None,
            options: dict[str, Any] | None = None,
            **kwargs: Any,
        ) -> str:
            return formatter(source, options or {})

        return wrapper


class FenceRegistry(UserDict[str, CustomFence]):
    """Custom dictionary for managing fences with automatic superfences registration."""

    def __setitem__(self, key: str, value: CustomFence) -> None:
        """Register fence in the registry."""
        super().__setitem__(key, value)

    def __delitem__(self, key: str) -> None:
        """Remove fence from the registry."""
        super().__delitem__(key)

    def add(self, fence: CustomFence) -> None:
        """Add a fence to the registry."""
        self[fence.name] = fence

    def remove(self, name: str) -> None:
        """Remove a fence from the registry."""
        if name in self:
            del self[name]

    def clear(self) -> None:
        """Clear all registered fences."""
        for key in list(self):
            del self[key]

    def descriptions(self) -> Iterator[tuple[str, str]]:
        """Yield name and description pairs for all fences."""
        yield from ((f.name, f.description) for f in self.values())

    def get_superfences_config(self) -> list[dict[str, Any]]:
        """Get the configuration for superfences."""
        return [fence.to_superfences_format() for fence in self.values()]


class SuperFence:
    """Base class for creating class-based custom fences."""

    name: ClassVar[str] = ""
    description: ClassVar[str] = ""

    @classmethod
    def format(cls, content: str, options: dict[str, Any]) -> str:
        """Override this method to implement custom formatting."""
        msg = f"Class {cls.__name__} must implement format method"
        raise NotImplementedError(msg)

    @classmethod
    def __call__(cls, content: str, options: dict[str, Any]) -> str:
        """Format the fence content."""
        return cls.format(content, options)

    @classmethod
    def to_custom_fence(cls) -> CustomFence:
        """Convert this fence class to a CustomFence instance."""
        return CustomFence(name=cls.name, formatter=cls(), description=cls.description)
