"""Base classes for tree processors that manipulate HTML DOM."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, TypeVar
from xml.etree import ElementTree as ET


# Try to import lxml, but don't fail if it's not installed
try:
    from lxml import etree as lxml_etree

    LXML_AVAILABLE = True
except ImportError:
    LXML_AVAILABLE = False

    # Create a stub for type checking
    class lxml_etree:  # type: ignore  # noqa: N801
        class _Element:
            pass


# Generic type for tree elements
E = TypeVar("E")


class TreeProcessor[T](ABC):
    """Abstract base class for tree processors."""

    def __init__(self, priority: int = 100) -> None:
        """Initialize with a priority.

        Args:
            priority: Execution priority (higher runs earlier)
        """
        self._priority = priority

    @abstractmethod
    def process_tree(self, tree: T) -> T:
        """Process and potentially modify an HTML tree.

        Args:
            tree: The HTML DOM tree to process

        Returns:
            The processed tree (may be the same or a new tree)
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


class ETTreeProcessor(TreeProcessor[ET.Element]):
    """Base class for ElementTree-based tree processors."""

    @abstractmethod
    def process_tree(self, tree: ET.Element) -> ET.Element:
        """Process the ElementTree.

        Args:
            tree: The ElementTree to process

        Returns:
            The processed ElementTree
        """
        ...

    def find_elements(self, tree: ET.Element, path: str) -> list[ET.Element]:
        """Find elements in the tree using ElementPath syntax.

        Args:
            tree: The ElementTree to search
            path: The ElementPath expression

        Returns:
            List of matching elements
        """
        return tree.findall(path)

    def get_text_content(self, element: ET.Element) -> str:
        """Get all text content from an element, including child elements.

        Args:
            element: The element to extract text from

        Returns:
            The combined text content
        """
        return "".join(element.itertext())

    def set_attribute(self, element: ET.Element, name: str, value: str) -> None:
        """Set an attribute on an element.

        Args:
            element: The element to modify
            name: Attribute name
            value: Attribute value
        """
        element.set(name, value)

    def create_element(
        self, tag: str, text: str | None = None, attrib: dict[str, str] | None = None
    ) -> ET.Element:
        """Create a new element.

        Args:
            tag: Element tag name
            text: Optional text content
            attrib: Optional attributes

        Returns:
            The new element
        """
        element = ET.Element(tag, attrib or {})
        if text is not None:
            element.text = text
        return element


if LXML_AVAILABLE:

    class LXMLTreeProcessor(TreeProcessor[lxml_etree._Element]):
        """Base class for lxml-based tree processors."""

        @abstractmethod
        def process_tree(self, tree: lxml_etree._Element) -> lxml_etree._Element:
            """Process the lxml tree.

            Args:
                tree: The lxml tree to process

            Returns:
                The processed lxml tree
            """
            ...

        def find_elements(
            self, tree: lxml_etree._Element, xpath: str
        ) -> list[lxml_etree._Element]:
            """Find elements in the tree using XPath.

            Args:
                tree: The tree to search
                xpath: The XPath expression

            Returns:
                List of matching elements
            """
            result = tree.xpath(xpath)
            if isinstance(result, list):
                # XPath can return other types, but we only want elements
                return [e for e in result if isinstance(e, lxml_etree._Element)]
            return []

        def get_text_content(self, element: lxml_etree._Element) -> str:
            """Get all text content from an element, including child elements.

            Args:
                element: The element to extract text from

            Returns:
                The combined text content
            """
            return element.xpath("string()")

        def set_attribute(
            self, element: lxml_etree._Element, name: str, value: str
        ) -> None:
            """Set an attribute on an element.

            Args:
                element: The element to modify
                name: Attribute name
                value: Attribute value
            """
            element.attrib[name] = value

        def create_element(
            self, tag: str, text: str | None = None, attrib: dict[str, str] | None = None
        ) -> lxml_etree._Element:
            """Create a new element.

            Args:
                tag: Element tag name
                text: Optional text content
                attrib: Optional attributes

            Returns:
                The new element
            """
            element = lxml_etree.Element(tag, attrib or {})
            if text is not None:
                element.text = text
            return element

else:

    class LXMLTreeProcessor(ABC):  # type: ignore  # noqa: B024
        """Placeholder for lxml-based tree processors when lxml is not installed."""

        def __init__(self, *args: Any, **kwargs: Any) -> None:
            """Initialize but raise ImportError."""
            msg = (
                "lxml is not installed. Install it with 'pip install lxml' "
                "to use LXMLTreeProcessor."
            )
            raise ImportError(msg)
