# mkdown

[![PyPI License](https://img.shields.io/pypi/l/mkdown.svg)](https://pypi.org/project/mkdown/)
[![Package status](https://img.shields.io/pypi/status/mkdown.svg)](https://pypi.org/project/mkdown/)
[![Monthly downloads](https://img.shields.io/pypi/dm/mkdown.svg)](https://pypi.org/project/mkdown/)
[![Distribution format](https://img.shields.io/pypi/format/mkdown.svg)](https://pypi.org/project/mkdown/)
[![Wheel availability](https://img.shields.io/pypi/wheel/mkdown.svg)](https://pypi.org/project/mkdown/)
[![Python version](https://img.shields.io/pypi/pyversions/mkdown.svg)](https://pypi.org/project/mkdown/)
[![Implementation](https://img.shields.io/pypi/implementation/mkdown.svg)](https://pypi.org/project/mkdown/)
[![Releases](https://img.shields.io/github/downloads/phil65/mkdown/total.svg)](https://github.com/phil65/mkdown/releases)
[![Github Contributors](https://img.shields.io/github/contributors/phil65/mkdown)](https://github.com/phil65/mkdown/graphs/contributors)
[![Github Forks](https://img.shields.io/github/forks/phil65/mkdown)](https://github.com/phil65/mkdown/forks)
[![Github Issues](https://img.shields.io/github/issues/phil65/mkdown)](https://github.com/phil65/mkdown/issues)
[![Github Issues](https://img.shields.io/github/issues-pr/phil65/mkdown)](https://github.com/phil65/mkdown/pulls)
[![Github Watchers](https://img.shields.io/github/watchers/phil65/mkdown)](https://github.com/phil65/mkdown/watchers)
[![Github Stars](https://img.shields.io/github/stars/phil65/mkdown)](https://github.com/phil65/mkdown/stars)
[![Github Repository size](https://img.shields.io/github/repo-size/phil65/mkdown)](https://github.com/phil65/mkdown)
[![Github last commit](https://img.shields.io/github/last-commit/phil65/mkdown)](https://github.com/phil65/mkdown/commits)
[![Github release date](https://img.shields.io/github/release-date/phil65/mkdown)](https://github.com/phil65/mkdown/releases)
[![Github language count](https://img.shields.io/github/languages/count/phil65/mkdown)](https://github.com/phil65/mkdown)
[![Github commits this month](https://img.shields.io/github/commit-activity/m/phil65/mkdown)](https://github.com/phil65/mkdown)
[![Package status](https://codecov.io/gh/phil65/mkdown/branch/main/graph/badge.svg)](https://codecov.io/gh/phil65/mkdown/)
[![PyUp](https://pyup.io/repos/github/phil65/mkdown/shield.svg)](https://pyup.io/repos/github/phil65/mkdown/)

[Read the documentation!](https://phil65.github.io/mkdown/)

Markdown helpers and data models, shared by [docler](https://github.com/phil65/docler) and
other projects:

- **Models**: `Document` (markdown content + images + metadata, load from / export to markdown
  files and directories with YAML frontmatter), `Image`, and `TextChunk` (usable as a field in
  pydantic models).
- **Metadata comments**: create and parse invisible `<!-- docler:<type> {json} -->` markers for
  page breaks and chunk boundaries, and split markdown by page or chunk.
- **Markdown helpers**: table of contents extraction (`mkdown.elements.toc.get_toc`), custom
  pymdownx.superfences fences (`mkdown.elements.fences`), file-path to code-fence language
  mapping (`mkdown.syntax`), Mermaid diagram rendering via mermaid.ink
  (`mkdown.mermaid_image`).

## Installation

```bash
pip install mkdown
# Pillow, for Image.dimensions:
pip install "mkdown[image]"
```

## Quickstart

```python
from mkdown import Document, Image, create_page_break, split_markdown_by_page

content = (
    "# Page one\n" + create_page_break(2, newline_separators=1) + "# Page two\n![logo](logo.png)"
)
doc = Document(
    content=content,
    title="Example",
    images=[Image(id="logo", content=b"...", mime_type="image/png", filename="logo.png")],
)

print(doc.page_count)  # 1
print(split_markdown_by_page(doc.content))  # ['# Page one\n\n', '# Page two\n![logo](logo.png)']
print(doc.to_markdown(include_frontmatter=True))
```

`Document.from_file()`, `Document.from_directory()`, `Document.export_to_directory()` and
`Document.export_to_markdown_file()` are async and accept any `upath`-compatible path.

## Markdown Conventions for OCR Output

This project utilizes Markdown as the primary, self-contained format for storing OCR results and associated metadata. The goal is to have a single, versionable, human-readable file representing a processed document, simplifying pipeline management and data provenance.

We employ a hybrid approach, using different mechanisms for different types of metadata:

### 1. Metadata Comments (for Non-Visual Markers)

For metadata that should *not* affect the visual rendering of the Markdown (like page boundaries or page-level information), we use specially formatted HTML/XML comments.

**Format:**

```
<!-- docler:data_type {json_payload} -->
```

*   **`data_type`**: A string indicating the kind of metadata (e.g., `page_break`, `chunk_boundary`).
*   **`{json_payload}`**: A JSON object with the metadata key-value pairs, serialized compactly with sorted keys.

**Defined Types:**

*   **`page_break`**: Marks the transition *to* the specified page number. Placed immediately *before* the content of the new page.
    *   Example Payload: `{"next_page": 2}`
    *   Example Comment: `<!-- docler:page_break {"next_page":2} -->`
*   **`chunk_boundary`**: Marks a transition where a document should get chunked (semantically).
    *   Example Payload: `{"chunk_id": 1}`
    *   Example Comment: `<!-- docler:chunk_boundary {"chunk_id":1} -->`

### 2. HTML Figures (for Images and Diagrams)

For visual elements like images or diagrams, especially when they require richer metadata (like source code or bounding boxes), we use standard HTML structures within the Markdown. This allows direct association of metadata and handles complex data like code snippets gracefully.

**Structure:**

We typically use an HTML `<figure>` element:

```html
<figure data-docler-type="diagram" data-diagram-id="sysarch-01">
  <img src="images/system_architecture.png"
       alt="System Architecture Diagram"
       data-page-num="5"
       style="max-width: 100%; height: auto;"
       >
  <figcaption>Figure 2: High-level system data flow.</figcaption>
  <script type="text/docler-mermaid">
    graph LR
        A[Data Ingest] --> B(Processing Queue);
        B --> C{Main Processor};
        D --> F(API Endpoint);
  </script>
</figure>
```

*   **`<figure>`**: The container element.
    *   `data-docler-type`: Indicates the type of figure (e.g., `image`, `diagram`).
    *   Other `data-*` attributes can be added for figure-level metadata.
*   **`<img>`**: The visual representation.
    *   `src`, `alt`: Standard attributes.
    *   `data-*`: Used for image-specific metadata like `data-page-num`
    *   `style`: Optional for basic presentation.
*   **`<figcaption>`**: Optional standard HTML caption.
*   **`<script type="text/docler-...">`**: Used to embed source code or other complex textual data.
    *   The `type` attribute is custom (e.g., `text/docler-mermaid`, `text/docler-latex`) so browsers ignore it.
    *   The raw code/text is placed inside, preserving formatting.

### Rationale

*   **Comments** are used for page breaks and metadata because they are guaranteed *not* to interfere with Markdown rendering, ensuring purely structural information remains invisible.
*   **HTML Figures** are used for images/diagrams because HTML provides standard ways (`data-*`, nested elements like `<script>`) to directly associate rich, potentially complex or multi-line metadata (like source code) with the visual element itself.

### Utilities

Helpers for creating and parsing these comments live in `mkdown.markdown_utils` and are
re-exported from `mkdown`:

1. **Page Breaks**: `create_page_break()` or `create_metadata_comment()` with `PAGE_BREAK_TYPE`:
   ```python
   from mkdown import PAGE_BREAK_TYPE, create_metadata_comment, split_markdown_by_page

   page_break = create_metadata_comment(PAGE_BREAK_TYPE, {"next_page": 2})
   # <!-- docler:page_break {"next_page":2} -->
   pages = split_markdown_by_page(f"Page 1\n{page_break}\nPage 2")
   # ['Page 1\n', 'Page 2']
   ```

2. **Chunk Boundaries**: `create_chunk_boundary()` marks semantic chunks:
   ```python
   from mkdown import create_chunk_boundary, split_markdown_by_chunks

   chunk_marker = create_chunk_boundary(
       chunk_id=1,
       keywords=["introduction", "overview"],
       extra_data={"start_line": 10, "end_line": 25},
   )
   # <!-- docler:chunk_boundary {"chunk_id":1,"end_line":25,"keywords":["introduction","overview"],"start_line":10} -->
   chunks = split_markdown_by_chunks(f"{chunk_marker}\nIntro text")
   # [({'chunk_id': 1, ...}, 'Intro text')]
   ```
