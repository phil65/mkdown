"""Pure python interface for the comrak markdown parser."""

from __future__ import annotations

from typing import Any

from mkdown.parsers.base_parser import BaseParser


class ComrakParser(BaseParser):
    """Parser implementation using Comrak."""

    def __init__(
        self,
        # Extension options
        strikethrough: bool = True,
        tagfilter: bool = True,
        table: bool = True,
        autolink: bool = True,
        tasklist: bool = True,
        superscript: bool = True,
        header_ids: bool | None = None,
        footnotes: bool = True,
        description_lists: bool = True,
        front_matter_delimiter: str | None = None,
        multiline_block_quotes: bool = True,
        alerts: bool = True,
        math_dollars: bool = True,
        math_code: bool = True,
        wikilinks_title_after_pipe: bool = True,
        wikilinks_title_before_pipe: bool = True,
        underline: bool = True,
        subscript: bool = True,
        spoiler: bool = True,
        greentext: bool = True,
        # Parse options
        smart: bool = False,
        default_info_string: str | None = None,
        relaxed_tasklist_matching: bool = False,
        relaxed_autolinks: bool = False,
        # Render options
        hardbreaks: bool = False,
        github_pre_lang: bool = False,
        full_info_string: bool = False,
        width: int = 0,
        unsafe_: bool = False,
        escape: bool = False,
        sourcepos: bool = False,
        list_style: str = "-",  # One of "-", "+", "*"
        **kwargs: Any,
    ) -> None:
        """Initialize the Comrak parser with all available options."""
        import comrak

        # Set up extension options
        self._ext_opts = comrak.ExtensionOptions()  # pyright: ignore
        self._ext_opts.strikethrough = strikethrough
        self._ext_opts.tagfilter = tagfilter
        self._ext_opts.table = table
        self._ext_opts.autolink = autolink
        self._ext_opts.tasklist = tasklist
        self._ext_opts.superscript = superscript
        self._ext_opts.header_ids = header_ids
        self._ext_opts.footnotes = footnotes
        self._ext_opts.description_lists = description_lists
        self._ext_opts.front_matter_delimiter = front_matter_delimiter
        self._ext_opts.multiline_block_quotes = multiline_block_quotes
        self._ext_opts.alerts = alerts
        self._ext_opts.math_dollars = math_dollars
        self._ext_opts.math_code = math_code
        self._ext_opts.wikilinks_title_after_pipe = wikilinks_title_after_pipe
        self._ext_opts.wikilinks_title_before_pipe = wikilinks_title_before_pipe
        self._ext_opts.underline = underline
        self._ext_opts.subscript = subscript
        self._ext_opts.spoiler = spoiler
        self._ext_opts.greentext = greentext
        self._parse_opts = comrak.ParseOptions()  # pyright: ignore
        self._parse_opts.smart = smart
        self._parse_opts.default_info_string = default_info_string
        self._parse_opts.relaxed_tasklist_matching = relaxed_tasklist_matching
        self._parse_opts.relaxed_autolinks = relaxed_autolinks
        self._render_opts = comrak.RenderOptions()  # pyright: ignore
        self._render_opts.hardbreaks = hardbreaks
        self._render_opts.github_pre_lang = github_pre_lang
        self._render_opts.full_info_string = full_info_string
        self._render_opts.width = width
        self._render_opts.unsafe_ = unsafe_
        self._render_opts.escape = escape
        self._render_opts.sourcepos = sourcepos
        self._render_opts.list_style = {"-": 45, "+": 43, "*": 42}[list_style]

        # Store additional options
        self._kwargs = kwargs

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
        import comrak

        # If options provided, create updated option objects
        if options:
            import copy

            # Make copies of our option objects
            ext_opts = copy.deepcopy(self._ext_opts)
            parse_opts = copy.deepcopy(self._parse_opts)
            render_opts = copy.deepcopy(self._render_opts)

            # Update extension options
            ext_option_names = [
                "strikethrough",
                "tagfilter",
                "table",
                "autolink",
                "tasklist",
                "superscript",
                "header_ids",
                "footnotes",
                "description_lists",
                "front_matter_delimiter",
                "multiline_block_quotes",
                "alerts",
                "math_dollars",
                "math_code",
                "wikilinks_title_after_pipe",
                "wikilinks_title_before_pipe",
                "underline",
                "subscript",
                "spoiler",
                "greentext",
            ]

            for opt_name in ext_option_names:
                if opt_name in options and hasattr(ext_opts, opt_name):
                    setattr(ext_opts, opt_name, options[opt_name])

            # Update parse options
            for opt_name in [
                "smart",
                "default_info_string",
                "relaxed_tasklist_matching",
                "relaxed_autolinks",
            ]:
                if opt_name in options and hasattr(parse_opts, opt_name):
                    setattr(parse_opts, opt_name, options[opt_name])

            # Update render options
            for opt_name in [
                "hardbreaks",
                "github_pre_lang",
                "full_info_string",
                "width",
                "unsafe_",
                "escape",
                "sourcepos",
            ]:
                if opt_name in options and hasattr(render_opts, opt_name):
                    setattr(render_opts, opt_name, options[opt_name])

            # Handle list style separately
            if "list_style" in options:
                render_opts.list_style = {"-": 45, "+": 43, "*": 42}[
                    options["list_style"]
                ]

            return comrak.render_markdown(  # pyright: ignore
                markdown_text,
                extension_options=ext_opts,
                parse_options=parse_opts,
                render_options=render_opts,
            )

        # Use stored options for efficiency
        return comrak.render_markdown(  # pyright: ignore
            markdown_text,
            extension_options=self._ext_opts,
            parse_options=self._parse_opts,
            render_options=self._render_opts,
        )

    @property
    def name(self) -> str:
        """Get the name of the parser."""
        return "comrak"

    @property
    def features(self) -> set[str]:
        """Get the set of supported features."""
        features = {"basic_markdown", "fenced_code"}

        # Add features based on enabled options
        if self._ext_opts.strikethrough:
            features.add("strikethrough")
        if self._ext_opts.table:
            features.add("tables")
        if self._ext_opts.autolink:
            features.add("autolink")
        if self._ext_opts.tasklist:
            features.add("tasklists")
        if self._ext_opts.alerts:
            features.add("alerts")
        if self._ext_opts.math_dollars or self._ext_opts.math_code:
            features.add("math")
        if self._ext_opts.footnotes:
            features.add("footnotes")
        if self._ext_opts.description_lists:
            features.add("definition_lists")
        if self._ext_opts.front_matter_delimiter:
            features.add("front_matter")
        if self._ext_opts.multiline_block_quotes:
            features.add("multiline_blockquotes")
        if self._ext_opts.superscript:
            features.add("superscript")
        if self._ext_opts.subscript:
            features.add("subscript")
        if (
            self._ext_opts.wikilinks_title_after_pipe
            or self._ext_opts.wikilinks_title_before_pipe
        ):
            features.add("wikilinks")
        if self._ext_opts.header_ids:
            features.add("header_ids")
        if self._ext_opts.underline:
            features.add("underline")
        if self._ext_opts.spoiler:
            features.add("spoiler")
        if self._ext_opts.greentext:
            features.add("greentext")

        return features


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.DEBUG)

    parser = ComrakParser()
    print(parser.convert("# Test"))
