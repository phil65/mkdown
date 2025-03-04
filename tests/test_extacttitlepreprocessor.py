"""Tests for the ExtractTitleETProcessor."""

from __future__ import annotations

from xml.etree import ElementTree as ET

import markdown
import pytest

from mkdown.tree_processors.extract_title import ExtractTitleETProcessor


@pytest.fixture
def md():
    """Create a markdown instance with attr_list extension."""
    return markdown.Markdown(
        extensions=["attr_list"]
    )  # Add attr_list extension for handling attributes


@pytest.fixture
def processor():
    """Create an ExtractTitleETProcessor instance."""
    return ExtractTitleETProcessor()


def create_tree_from_html(html: str) -> ET.Element:
    """Create an ElementTree from HTML string."""
    return ET.fromstring(f"<root>{html}</root>")


def test_basic_title_extraction(processor: ExtractTitleETProcessor):
    """Test basic h1 title extraction."""
    html = "<h1>Simple Title</h1><p>Some content</p>"
    tree = create_tree_from_html(html)
    processor.process_tree(tree)
    assert processor.title == "Simple Title"


def test_no_title(processor: ExtractTitleETProcessor):
    """Test behavior when no h1 title is present."""
    html = "<h2>Secondary Title</h2><p>Some content</p>"
    tree = create_tree_from_html(html)
    processor.process_tree(tree)
    assert processor.title is None


def test_multiple_h1_takes_first(processor: ExtractTitleETProcessor):
    """Test that only the first h1 is used as title."""
    html = "<h1>First Title</h1><p>Content</p><h1>Second Title</h1>"
    tree = create_tree_from_html(html)
    processor.process_tree(tree)
    assert processor.title == "First Title"


def test_complex_title(processor: ExtractTitleETProcessor):
    """Test title with formatting."""
    html = "<h1>Title with <em>italic</em> and <strong>bold</strong></h1><p>Content</p>"
    tree = create_tree_from_html(html)
    processor.process_tree(tree)
    assert processor.title == "Title with italic and bold"


def test_title_with_anchor(processor: ExtractTitleETProcessor):
    """Test title with anchor link."""
    html = '<h1 id="anchor">Title with anchor</h1><p>Content</p>'
    tree = create_tree_from_html(html)
    processor.process_tree(tree)
    assert processor.title == "Title with anchor"


def test_empty_title(processor: ExtractTitleETProcessor):
    """Test empty h1 tag."""
    html = "<h1></h1><p>Content</p>"
    tree = create_tree_from_html(html)
    processor.process_tree(tree)
    assert processor.title == ""


def test_title_with_multiple_lines(processor: ExtractTitleETProcessor):
    """Test title in a single h1 tag."""
    html = "<h1>Title that spans multiple lines</h1><p>Content</p>"
    tree = create_tree_from_html(html)
    processor.process_tree(tree)
    assert processor.title == "Title that spans multiple lines"


def test_title_with_special_characters(processor: ExtractTitleETProcessor):
    """Test title with special characters."""
    html = "<h1>Title with $pecial &amp; &lt;chars&gt;</h1><p>Content</p>"
    tree = create_tree_from_html(html)
    processor.process_tree(tree)
    assert processor.title == "Title with $pecial & <chars>"


def test_subsequent_conversions(processor: ExtractTitleETProcessor):
    """Test that processor works correctly for multiple conversions."""
    html1 = "<h1>First Document</h1><p>Content</p>"
    tree1 = create_tree_from_html(html1)
    processor.process_tree(tree1)
    assert processor.title == "First Document"

    html2 = "<h2>Second Document</h2><p>Content</p>"
    tree2 = create_tree_from_html(html2)
    processor.process_tree(tree2)
    # Since h2 isn't an h1, title shouldn't change
    assert processor.title == "First Document"

    html3 = "<h1>Third Document</h1><p>Content</p>"
    tree3 = create_tree_from_html(html3)
    processor.process_tree(tree3)
    assert processor.title == "Third Document"
