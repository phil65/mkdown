"""Tree processors for extracting document title from the first heading."""

from __future__ import annotations

import copy
from typing import TYPE_CHECKING

from mkdown.tree_processors.base import ETTreeProcessor


if TYPE_CHECKING:
    from xml.etree import ElementTree as ET


# Try to import lxml, but don't fail if it's not installed
try:
    from lxml import etree as lxml_etree  # pyright: ignore

    from mkdown.tree_processors.base import LXMLTreeProcessor

    LXML_AVAILABLE = True
except ImportError:
    LXML_AVAILABLE = False  # type: ignore

    # Create a stub for type checking
    class lxml_etree:  # type: ignore  # noqa: N801
        class _Element:
            pass

    LXMLTreeProcessor = object  # type: ignore


class ExtractTitleETProcessor(ETTreeProcessor):
    """Extract title from the first h1 element using ElementTree."""

    def __init__(self, priority: int = -10) -> None:
        """Initialize with a low priority to run near the end.

        Args:
            priority: Execution priority (lower runs later)
        """
        super().__init__(priority)
        self.title: str | None = None

    def process_tree(self, tree: ET.Element) -> ET.Element:
        """Extract title from the first h1 element.

        Args:
            tree: The HTML DOM tree

        Returns:
            The unchanged tree
        """
        try:
            # Find the first h1 element
            h1_elements = self.find_elements(tree, ".//h1")
            if not h1_elements:
                return tree

            h1 = h1_elements[0]

            # Handle trailing anchor if present (common in some markdown renderers)
            if len(h1) > 0 and h1[-1].tag == "a" and not (h1[-1].tail or "").strip():
                h1 = copy.copy(h1)
                h1.remove(h1[-1])

            # Extract all text content
            title = self.get_text_content(h1)
            self.title = title.strip()

        except Exception as e:  # noqa: BLE001
            # Log but don't fail if title extraction has an issue
            import logging

            logging.getLogger(__name__).warning("Error extracting title: %s", e)

        return tree


if LXML_AVAILABLE:

    class ExtractTitleLXMLProcessor(LXMLTreeProcessor):
        """Extract title from the first h1 element using lxml."""

        def __init__(self, priority: int = -10) -> None:
            """Initialize with a low priority to run near the end.

            Args:
                priority: Execution priority (lower runs later)
            """
            super().__init__(priority)
            self.title: str | None = None

        def process_tree(self, tree: lxml_etree._Element) -> lxml_etree._Element:
            """Extract title from the first h1 element.

            Args:
                tree: The HTML DOM tree

            Returns:
                The unchanged tree
            """
            try:
                # Find the first h1 element
                h1_elements = self.find_elements(tree, "//h1")
                if not h1_elements:
                    return tree

                h1 = h1_elements[0]

                # Handle trailing anchor if present (common in some markdown renderers)
                children = h1.getchildren()
                if (
                    children
                    and children[-1].tag == "a"
                    and not (children[-1].tail or "").strip()
                ):
                    h1 = copy.deepcopy(h1)  # Create copy to avoid modifying original
                    h1.remove(children[-1])

                # Extract all text content
                title = self.get_text_content(h1)
                self.title = title.strip()

            except Exception as e:  # noqa: BLE001
                # Log but don't fail if title extraction has an issue
                import logging

                logging.getLogger(__name__).warning("Error extracting title: %s", e)

            return tree
