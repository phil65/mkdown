from __future__ import annotations

import re

import pyromark
from pyromark._options import Options


def markdown_to_html(
    markdown_text: str,
    *,
    # Pre-processing options
    convert_admonitions: bool = True,
    # pyromark Options flags
    enable_tables: bool = False,
    enable_footnotes: bool = False,
    enable_strikethrough: bool = False,
    enable_tasklists: bool = False,
    enable_smart_punctuation: bool = False,
    enable_heading_attributes: bool = False,
    enable_yaml_style_metadata_blocks: bool = False,
    enable_pluses_delimited_metadata_blocks: bool = False,
    enable_old_footnotes: bool = False,
    enable_math: bool = False,
    enable_gfm: bool = True,  # Enable GFM by default for admonition support
    enable_definition_list: bool = False,
    enable_superscript: bool = False,
    enable_subscript: bool = False,
    enable_wikilinks: bool = False,
) -> str:
    """Convert markdown to HTML with pre-processing for admonitions.

    Args:
        markdown_text: Input markdown text
        convert_admonitions: Whether to convert MkDocs admonitions to GFM alerts
        enable_tables: Enable tables extension
        enable_footnotes: Enable footnotes extension
        enable_strikethrough: Enable strikethrough extension
        enable_tasklists: Enable tasklists extension
        enable_smart_punctuation: Enable smart punctuation
        enable_heading_attributes: Enable heading attributes extension
        enable_yaml_style_metadata_blocks: Enable YAML-style metadata blocks
        enable_pluses_delimited_metadata_blocks: Enable plus-delimited metadata blocks
        enable_old_footnotes: Enable old footnotes style
        enable_math: Enable math extension
        enable_gfm: Enable GitHub Flavored Markdown (defaults to True)
        enable_definition_list: Enable definition lists
        enable_superscript: Enable superscript extension
        enable_subscript: Enable subscript extension
        enable_wikilinks: Enable wikilinks extension

    Returns:
        HTML output
    """
    # Build options flag
    options = Options(0)

    if enable_tables:
        options |= Options.ENABLE_TABLES
    if enable_footnotes:
        options |= Options.ENABLE_FOOTNOTES
    if enable_strikethrough:
        options |= Options.ENABLE_STRIKETHROUGH
    if enable_tasklists:
        options |= Options.ENABLE_TASKLISTS
    if enable_smart_punctuation:
        options |= Options.ENABLE_SMART_PUNCTUATION
    if enable_heading_attributes:
        options |= Options.ENABLE_HEADING_ATTRIBUTES
    if enable_yaml_style_metadata_blocks:
        options |= Options.ENABLE_YAML_STYLE_METADATA_BLOCKS
    if enable_pluses_delimited_metadata_blocks:
        options |= Options.ENABLE_PLUSES_DELIMITED_METADATA_BLOCKS
    if enable_old_footnotes:
        options |= Options.ENABLE_OLD_FOOTNOTES
    if enable_math:
        options |= Options.ENABLE_MATH
    if enable_gfm:
        options |= Options.ENABLE_GFM
    if enable_definition_list:
        options |= Options.ENABLE_DEFINITION_LIST
    if enable_superscript:
        options |= Options.ENABLE_SUPERSCRIPT
    if enable_subscript:
        options |= Options.ENABLE_SUBSCRIPT
    if enable_wikilinks:
        options |= Options.ENABLE_WIKILINKS

    # Apply pre-processing if enabled
    preprocessed_text = markdown_text
    if convert_admonitions:
        preprocessed_text = convert_mkdocs_to_gfm_admonitions(preprocessed_text)

    # Convert to HTML using pyromark
    return pyromark.html(preprocessed_text, options=options)


def convert_mkdocs_to_gfm_admonitions(markdown_text: str) -> str:
    """Convert MkDocs-style admonitions to GitHub Flavored Markdown alerts.

    Handles the format:
    !!! type ["optional title"]
        content on
        multiple lines

    And converts to:
    > [!TYPE] optional title
    > content on
    > multiple lines
    """
    # Pattern matches admonitions with an optional title
    # Group 1: The admonition type (info, note, etc.)
    # Group 2: Optional title in quotes (or None if not present)
    # Group 3: Content (indented with 4 spaces)
    pattern = r'!!! (\w+)(?:\s+"([^"]*)")?\s*\n((?:    .*(?:\n|$))*)'

    def replacement(match):
        admonition_type = match.group(1).upper()

        # Mapping of MkDocs admonition types to GFM alert types
        type_mapping = {
            "NOTE": "NOTE",
            "INFO": "NOTE",
            "TIP": "TIP",
            "HINT": "TIP",
            "IMPORTANT": "IMPORTANT",
            "WARNING": "WARNING",
            "CAUTION": "WARNING",
            "DANGER": "CAUTION",
            "ERROR": "CAUTION",
            # Add other mappings as needed
        }

        gfm_type = type_mapping.get(admonition_type, "NOTE")

        # Get content and remove the 4-space indentation
        title = match.group(2) or ""
        content = match.group(3)
        content_lines = []

        for line in content.split("\n"):
            if line.startswith("    "):
                content_lines.append(line[4:])
            elif not line:
                content_lines.append("")
            else:
                content_lines.append(line)

        # Build the GFM alert format
        gfm_alert = f"> [!{gfm_type}]"
        if title:
            gfm_alert += f" {title}"
        gfm_alert += "\n"

        # Add content with each line prefixed by "> "
        gfm_content = "\n".join(f"> {line}" if line else ">" for line in content_lines)
        gfm_alert += gfm_content

        return gfm_alert

    return re.sub(pattern, replacement, markdown_text, flags=re.MULTILINE)
