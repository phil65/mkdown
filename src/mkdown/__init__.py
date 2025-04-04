"""A Python wrapper for Rust-based markdown parsers with processor support."""

__version__ = "0.11.5"

from mkdown.parsers.base_parser import BaseParser
from mkdown.parsers.parser import MarkdownParser
from mkdown.parsers.comrak_parser import ComrakParser
from mkdown.parsers.github_api_parser import GithubApiParser
from mkdown.parsers.markdown2_parser import Markdown2Parser
from mkdown.parsers.markdown_it_pyrs_parser import MarkdownItPyRSParser
from mkdown.parsers.marko_parser import MarkoParser
from mkdown.parsers.mistune_parser import MistuneParser
from mkdown.parsers.pyromark_parser import PyroMarkParser
from mkdown.parsers.python_markdown_parser import PythonMarkdownParser

from mkdown.pre_processors.base import PreProcessor
from mkdown.pre_processors.admonition_converter import MkDocsToGFMAdmonitionProcessor

from mkdown.tree_processors.base import ETTreeProcessor, LXMLTreeProcessor, TreeProcessor
from mkdown.tree_processors.extract_title import ExtractTitleETProcessor
from mkdown.tree_processors.extract_title_lxml import ExtractTitleLXMLProcessor

from mkdown.post_processors.base import PostProcessor
from mkdown.post_processors.sanitizer import SanitizeHTMLProcessor

__all__ = [
    "BaseParser",
    "ComrakParser",
    "ETTreeProcessor",
    "ExtractTitleETProcessor",
    "ExtractTitleLXMLProcessor",
    "GithubApiParser",
    "LXMLTreeProcessor",
    "Markdown2Parser",
    "MarkdownItPyRSParser",
    "MarkdownParser",
    "MarkoParser",
    "MistuneParser",
    "MkDocsToGFMAdmonitionProcessor",
    "PostProcessor",
    "PreProcessor",
    "PyroMarkParser",
    "PythonMarkdownParser",
    "SanitizeHTMLProcessor",
    "TreeProcessor",
]
