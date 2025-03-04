"""Pure python interface for the comrak markdown parser."""

from __future__ import annotations

from typing import Any


def markdown_to_html(
    markdown_text: str,
    *,
    strikethrough: bool = False,
    tagfilter: bool = False,
    table: bool = False,
    autolink: bool = False,
    tasklist: bool = False,
    superscript: bool = False,
    header_ids: bool | None = None,
    footnotes: bool = False,
    description_lists: bool = False,
    front_matter_delimiter: str | None = None,
    multiline_block_quotes: bool = False,
    alerts: bool = True,  # GFM alerts enabled by default
    math: bool = False,
    shortcodes: bool = False,
    wikilinks: bool = False,
    underline: bool = False,
    subscript: bool = False,
    spoiler: bool = False,
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
) -> str:
    """Convert markdown to HTML with configurable options.

    Args:
        markdown_text: Input markdown text
        convert_mkdocs_admonitions: Pre-process MkDocs style admonitions to GFM alerts
        # Extension options
        strikethrough: Enable strikethrough syntax
        tagfilter: Enable HTML tag filtering
        table: Enable GFM tables
        autolink: Enable autolinking
        tasklist: Enable GFM task lists
        superscript: Enable superscript syntax
        header_ids: Add IDs to headers
        footnotes: Enable footnotes
        description_lists: Enable description lists
        front_matter_delimiter: Front matter delimiter
        multiline_block_quotes: Enable multiline blockquotes
        alerts: Enable GFM alerts (default: True)
        math: Enable math syntax
        shortcodes: Enable shortcodes
        wikilinks: Enable wiki-style links
        underline: Enable underline syntax
        subscript: Enable subscript syntax
        spoiler: Enable spoiler blocks
        # Parse options
        smart: Enable smart punctuation
        default_info_string: Default info string for code blocks
        relaxed_tasklist_matching: Relaxed task list matching
        relaxed_autolinks: Relaxed autolink parsing
        # Render options
        hardbreaks: Render soft breaks as hard breaks
        github_pre_lang: Use GitHub-style code block language
        full_info_string: Include full info string in code blocks
        width: Wrap width (0 for no wrapping)
        unsafe_: Allow raw HTML and dangerous URLs
        escape: Escape HTML tags
        sourcepos: Include source position info
        list_style: List marker style ("-", "+", "*")
        kwargs: Additional keyword arguments

    Returns:
        HTML output as string
    """
    import comrak

    # Pre-process MkDocs admonitions if requested
    text = markdown_text
    # Set up extension options
    ext_opts = comrak.ExtensionOptions()
    ext_opts.strikethrough = strikethrough
    ext_opts.tagfilter = tagfilter
    ext_opts.table = table
    ext_opts.autolink = autolink
    ext_opts.tasklist = tasklist
    ext_opts.superscript = superscript
    ext_opts.header_ids = header_ids
    ext_opts.footnotes = footnotes
    ext_opts.description_lists = description_lists
    ext_opts.front_matter_delimiter = front_matter_delimiter
    ext_opts.multiline_block_quotes = multiline_block_quotes
    ext_opts.alerts = alerts
    ext_opts.math = math
    ext_opts.shortcodes = shortcodes
    ext_opts.wikilinks = wikilinks
    ext_opts.underline = underline
    ext_opts.subscript = subscript
    ext_opts.spoiler = spoiler

    # Set up parse options
    parse_opts = comrak.ParseOptions()
    parse_opts.smart = smart
    parse_opts.default_info_string = default_info_string
    parse_opts.relaxed_tasklist_matching = relaxed_tasklist_matching
    parse_opts.relaxed_autolinks = relaxed_autolinks

    # Set up render options
    render_opts = comrak.RenderOptions()
    render_opts.hardbreaks = hardbreaks
    render_opts.github_pre_lang = github_pre_lang
    render_opts.full_info_string = full_info_string
    render_opts.width = width
    render_opts.unsafe_ = unsafe_
    render_opts.escape = escape
    render_opts.sourcepos = sourcepos
    render_opts.list_style = {"-": 45, "+": 43, "*": 42}[list_style]

    # Convert to HTML
    return comrak.render_markdown(
        text,
        extension_options=ext_opts,
        parse_options=parse_opts,
        render_options=render_opts,
    )
