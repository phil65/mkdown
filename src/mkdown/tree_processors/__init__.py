"""Tree processors for HTML DOM manipulation."""

from mkdown.tree_processors.base import TreeProcessor, ETTreeProcessor
from mkdown.tree_processors.extract_title import ExtractTitleETProcessor
from mkdown.tree_processors.registry import TreeProcessorRegistry

# Import lxml processors only if lxml is available
try:
    from mkdown.tree_processors.base import LXMLTreeProcessor
    from mkdown.tree_processors.extract_title_lxml import ExtractTitleLXMLProcessor

    HAS_LXML = True
except ImportError:
    # Create placeholder classes when lxml is not available
    HAS_LXML = False

    # These will be imported but will raise ImportError when instantiated
    LXMLTreeProcessor = None  # type: ignore
    ExtractTitleLXMLProcessor = None  # type: ignore

__all__ = [
    "ETTreeProcessor",
    "ExtractTitleETProcessor",
    "ExtractTitleLXMLProcessor",
    "LXMLTreeProcessor",
    "TreeProcessor",
    "TreeProcessorRegistry",
]
