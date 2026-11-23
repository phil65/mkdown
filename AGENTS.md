# AGENTS.md

## Overview

`mkdown` is a small library of Markdown helpers and data models. Its core is a set of
pydantic models (`Document`, `Image`) plus the `TextChunk` dataclass, and utilities for the
"docler" Markdown conventions: invisible metadata comments such as
`<!-- docler:page_break {"next_page":2} -->`. It is a dependency of docler, chatly, mknodes and
other packages, so keep the public API (everything in `src/mkdown/__init__.py`) stable.

## Architecture

- `src/mkdown/__init__.py`: public re-exports (models + `markdown_utils` functions/constants).
- `src/mkdown/models/`
  - `document.py`: `Document(schemez.Schema)`: markdown `content` with internal image references,
    `images: list[Image]`, metadata fields. Loads from a markdown file/directory (YAML frontmatter,
    `![id](url)` image refs) and exports to markdown file/directory (`to_markdown`,
    `export_to_directory`, `export_to_markdown_file`). `page_count` counts page-break comments.
  - `image.py`: `Image(schemez.Schema)`: bytes or base64 content, `to_base64[_url]`, async
    `from_file`, `dimensions` (needs the optional `image` extra / Pillow).
  - `textchunk.py`: `TextChunk` dataclass (chunk of a document with images/metadata).
    `Image` is imported at runtime on purpose so pydantic can build models nesting `TextChunk`
    (regression test in `tests/test_textchunk.py`).
- `src/mkdown/markdown_utils.py`: create/parse metadata comments (`create_metadata_comment`,
  `parse_metadata_comments`), page breaks, chunk boundaries, `split_markdown_by_page`,
  `split_markdown_by_chunks`, `create_image_reference`. Comment payloads are compact,
  key-sorted JSON (stdlib `json`); parsing uses `anyenv.load_json`.
- `src/mkdown/elements/toc.py`: `get_toc()` builds a `TableOfContents` of `AnchorLink`s via
  Python-Markdown's `toc` extension.
- `src/mkdown/elements/fences.py`: `CustomFence`, `FenceRegistry`, `SuperFence` for
  pymdownx.superfences custom fences.
- `src/mkdown/extensions.py`: dataclasses mirroring Python-Markdown extension configs
  (`TocConfig`, `FencedCodeConfig`, ...).
- `src/mkdown/syntax.py`: file path -> code-fence language mapping, `format_code_block`,
  `format_file_content`.
- `src/mkdown/mermaid_image.py`: `mermaid_image()` renders a Mermaid diagram via the
  mermaid.ink web service (httpx2, network access).
- `src/mkdown/log.py`: `get_logger()`.
- `benchmark/`: parser benchmark scripts (currently stale: imports a removed
  `mkdown.parsers` module).

## Where to look

| Task | File |
| --- | --- |
| Public API / exports | `src/mkdown/__init__.py` |
| Document load/export, frontmatter | `src/mkdown/models/document.py` |
| Image handling | `src/mkdown/models/image.py` |
| Chunk model | `src/mkdown/models/textchunk.py` |
| Metadata comments, page breaks, chunk boundaries | `src/mkdown/markdown_utils.py` |
| Table of contents | `src/mkdown/elements/toc.py` |
| Custom fences | `src/mkdown/elements/fences.py` |
| Tests | `tests/` |
| CI | `.github/workflows/build.yml`, `.github/workflows/documentation.yml` |
| Dev tasks | `duties.py` |

## Commands

```bash
uv sync --all-extras                # setup (default groups: dev, lint, docs)
uv run pytest                       # tests
uvx ruff check . && uvx ruff format --check .   # lint/format (CI uses newest ruff)
uv run ty check                     # type check (src only, warnings fail)
uv run deptry src                   # dependency hygiene
uv run mkdocs-mknodes build         # docs build (CI: documentation.yml)
uv build                            # package
uv run duty lint | lint_check | test | build | serve | update   # duties.py shortcuts
```

Pre-commit hooks (`.pre-commit-config.yaml`) run tombi, ruff, ty and pytest on commit.

## Conventions

- Python >= 3.13, `from __future__ import annotations` everywhere; ruff with an extensive rule
  set (`pyproject.toml`), line length 100, Google-style docstrings.
- Imports only needed for annotations go under `TYPE_CHECKING`, except types pydantic must
  resolve at runtime (fields of pydantic models / dataclasses used in pydantic models).
  Ruff's TC rules treat `pydantic.BaseModel` and `schemez.Schema` subclasses as runtime-evaluated.
- Use targeted `# ty: ignore[rule]` only for genuine checker limitations.
- Tests are plain pytest functions in `tests/test_*.py`.
- File I/O goes through `upath.UPath` / `upathtools` (supports fsspec paths).

## Pitfalls

- Copier-managed project (`.copier-answers.yml`, template `phil65/copier-phil65`). Workflows,
  `duties.py`, `.pre-commit-config.yaml`, most of `pyproject.toml` and `mkdocs.yml` come from the
  template; prefer `copier update` over hand edits. Add dependencies below the
  `# Only add below (Copier)` markers.
- Every runtime import must be declared in `dependencies` (check with `uv run deptry src`);
  lazy imports like `yaml`, `markdown`, `httpx2` are still runtime dependencies.
- Pillow is optional (`image` extra); `Image.dimensions` returns `None` without it.
- The metadata comment format (`<!-- docler:<type> {json} -->`, prefix `DEFAULT_PREFIX`) is
  parsed by downstream projects: don't change its shape.
- `mermaid_image()` needs network access; don't call it in tests.
- Docs site is the mkdocs-mknodes default site (README + generated API pages); `docs/` is empty.
