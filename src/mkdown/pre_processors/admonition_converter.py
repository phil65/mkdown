"""Preprocessor that converts MkDocs-style admonitions to GFM alerts."""

from __future__ import annotations

import re

from mkdown.pre_processors.base import PreProcessor


class MkDocsToGFMAdmonitionProcessor(PreProcessor):
    """Convert MkDocs-style admonitions to GitHub Flavored Markdown alerts."""

    def __init__(self, priority: int = 50) -> None:
        """Initialize with a default priority.

        Args:
            priority: Execution priority (higher runs earlier)
        """
        super().__init__(priority)
        self._pattern = re.compile(
            r'!!! (\w+)(?:\s+"([^"]*)")?\s*\n((?:    .*(?:\n|$))*)', flags=re.MULTILINE
        )
        self._type_mapping = {
            "NOTE": "NOTE",
            "INFO": "NOTE",
            "TIP": "TIP",
            "HINT": "TIP",
            "IMPORTANT": "IMPORTANT",
            "WARNING": "WARNING",
            "CAUTION": "WARNING",
            "DANGER": "CAUTION",
            "ERROR": "CAUTION",
        }

    def process_markdown(self, markdown: str) -> str:
        """Convert MkDocs-style admonitions to GitHub Flavored Markdown alerts.

        Handles the format:
        !!! type ["optional title"]
            content on
            multiple lines

        And converts to:
        > [!TYPE] optional title
        > content on
        > multiple lines

        Args:
            markdown: The markdown text to process

        Returns:
            The processed markdown text with converted admonition syntax
        """
        return self._pattern.sub(self._replace_admonition, markdown)

    def _replace_admonition(self, match: re.Match) -> str:
        """Replace a matched admonition with GFM alert syntax.

        Args:
            match: The regex match object

        Returns:
            The converted GFM alert syntax
        """
        admonition_type = match.group(1).upper()
        gfm_type = self._type_mapping.get(admonition_type, "NOTE")

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

    @classmethod
    def convert_text(cls, markdown: str) -> str:
        """Utility method to convert a markdown text without creating an instance.

        Args:
            markdown: The markdown text to process

        Returns:
            The processed markdown text
        """
        processor = cls()
        return processor.process_markdown(markdown)
