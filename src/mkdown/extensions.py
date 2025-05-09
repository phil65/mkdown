from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from collections.abc import Callable


# https://python-markdown.github.io/extensions/api/
# FrontMatter / Meta


@dataclass
class TocConfig:
    """Default configuration options."""

    marker: str = "[TOC]"
    """Text to find and replace with Table of Contents. Set to empty string to disable."""

    title: str = ""
    """Title to insert into TOC `<div>`."""

    title_class: str = "toctitle"
    """CSS class used for the title."""

    toc_class: str = "toc"
    """CSS class(es) used for the TOC."""

    anchorlink: bool = False
    """True if header should be a self link."""

    anchorlink_class: str = "toclink"
    """CSS class(es) used for the anchor link."""

    permalink: bool | str = False
    """True or link text if a Sphinx-style permalink should be added."""

    permalink_class: str = "headerlink"
    """CSS class(es) used for the permalink."""

    permalink_title: str = "Permanent link"
    """Title attribute of the permalink."""

    permalink_leading: bool = False
    """True if permalinks should be placed at start of the header, rather than end."""

    baselevel: str = "1"
    """Base level for headers."""

    slugify: Callable | None = None  # Will be set in __init__
    """Function to generate anchors based on header text."""

    separator: str = "-"
    """Word separator."""

    toc_depth: int | str = 6
    """Define the range of section levels to include in the Table of Contents.
    A single integer (b) defines the bottom section level (<h1>..<hb>) only.
    A string consisting of two digits separated by a hyphen ('2-5') defines
    the top (t) and the bottom (b) (<ht>..<hb>)."""


@dataclass
class FencedCodeConfig:
    """Default configuration options."""

    lang_prefix: str = "language-"
    """Prefix prepended to the language."""
