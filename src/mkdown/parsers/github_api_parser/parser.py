"""Github API markdown parser."""

from __future__ import annotations

from typing import Any, Literal

from mkdown.parsers.base_parser import BaseParser


class GithubApiParser(BaseParser):
    """Parser implementation using Github API."""

    def __init__(
        self,
        # Extension options
        mode: Literal["markdown", "gfm"] = "markdown",
        context: str | None = None,
    ) -> None:
        self.mode = mode
        self.context = context

    def convert(self, markdown_text: str, **options: Any) -> str:
        """Convert markdown to HTML.

        Uses pre-configured options for performance when no overrides are provided.
        Only creates new option objects when specific settings need to be changed.

        Args:
            markdown_text: Input markdown text
            **options: Override default options for this conversion

        Returns:
            HTML output as string
        """
        import httpx

        json = {"mode": self.mode, "text": markdown_text}
        if self.context:
            json["context"] = self.context
        response = httpx.post("https://api.github.com/markdown", json=json)
        if response.status_code != 200:  # noqa: PLR2004
            msg = f"Failed to convert markdown to HTML: {response.text}"
            raise RuntimeError(msg)
        return response.text

    @property
    def name(self) -> str:
        """Get the name of the parser."""
        return "comrak"

    @property
    def features(self) -> set[str]:
        """Get the set of supported features."""
        return {"basic_markdown", "fenced_code"}


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.DEBUG)

    parser = GithubApiParser()
    print(parser.convert("# Test"))
