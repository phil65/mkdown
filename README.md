# mkdown

[![PyPI License](https://img.shields.io/pypi/l/mkdown.svg)](https://pypi.org/project/mkdown/)
[![Package status](https://img.shields.io/pypi/status/mkdown.svg)](https://pypi.org/project/mkdown/)
[![Daily downloads](https://img.shields.io/pypi/dd/mkdown.svg)](https://pypi.org/project/mkdown/)
[![Weekly downloads](https://img.shields.io/pypi/dw/mkdown.svg)](https://pypi.org/project/mkdown/)
[![Monthly downloads](https://img.shields.io/pypi/dm/mkdown.svg)](https://pypi.org/project/mkdown/)
[![Distribution format](https://img.shields.io/pypi/format/mkdown.svg)](https://pypi.org/project/mkdown/)
[![Wheel availability](https://img.shields.io/pypi/wheel/mkdown.svg)](https://pypi.org/project/mkdown/)
[![Python version](https://img.shields.io/pypi/pyversions/mkdown.svg)](https://pypi.org/project/mkdown/)
[![Implementation](https://img.shields.io/pypi/implementation/mkdown.svg)](https://pypi.org/project/mkdown/)
[![Releases](https://img.shields.io/github/downloads/phil65/mkdown/total.svg)](https://github.com/phil65/mkdown/releases)
[![Github Contributors](https://img.shields.io/github/contributors/phil65/mkdown)](https://github.com/phil65/mkdown/graphs/contributors)
[![Github Discussions](https://img.shields.io/github/discussions/phil65/mkdown)](https://github.com/phil65/mkdown/discussions)
[![Github Forks](https://img.shields.io/github/forks/phil65/mkdown)](https://github.com/phil65/mkdown/forks)
[![Github Issues](https://img.shields.io/github/issues/phil65/mkdown)](https://github.com/phil65/mkdown/issues)
[![Github Issues](https://img.shields.io/github/issues-pr/phil65/mkdown)](https://github.com/phil65/mkdown/pulls)
[![Github Watchers](https://img.shields.io/github/watchers/phil65/mkdown)](https://github.com/phil65/mkdown/watchers)
[![Github Stars](https://img.shields.io/github/stars/phil65/mkdown)](https://github.com/phil65/mkdown/stars)
[![Github Repository size](https://img.shields.io/github/repo-size/phil65/mkdown)](https://github.com/phil65/mkdown)
[![Github last commit](https://img.shields.io/github/last-commit/phil65/mkdown)](https://github.com/phil65/mkdown/commits)
[![Github release date](https://img.shields.io/github/release-date/phil65/mkdown)](https://github.com/phil65/mkdown/releases)
[![Github language count](https://img.shields.io/github/languages/count/phil65/mkdown)](https://github.com/phil65/mkdown)
[![Github commits this week](https://img.shields.io/github/commit-activity/w/phil65/mkdown)](https://github.com/phil65/mkdown)
[![Github commits this month](https://img.shields.io/github/commit-activity/m/phil65/mkdown)](https://github.com/phil65/mkdown)
[![Github commits this year](https://img.shields.io/github/commit-activity/y/phil65/mkdown)](https://github.com/phil65/mkdown)
[![Package status](https://codecov.io/gh/phil65/mkdown/branch/main/graph/badge.svg)](https://codecov.io/gh/phil65/mkdown/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PyUp](https://pyup.io/repos/github/phil65/mkdown/shield.svg)](https://pyup.io/repos/github/phil65/mkdown/)

[Read the documentation!](https://phil65.github.io/mkdown/)


| Feature | Python-Markdown | Markdown2 | Mistune | Comrak (Rust) | PyroMark (Rust) | Markdown-It-PyRS (Rust) |
|---------|----------------|-----------|---------|---------------|-----------------|-------------------------|
| **Core CommonMark** | ✅ | ✅ | ✅ | ✅ (100% compliant) | ✅ | ✅ (100% compliant) |
| Fenced code blocks | ✅ | ✅ (with ext) | ✅ | ✅ | ✅ | ✅ |
| **GitHub Flavored Markdown** |||||||
| Tables | ✅ (with ext) | ✅ (with ext) | ✅ (with plugin) | ✅ (with `.table`) | ✅ (optional) | ✅ (with GFM or `.table`) |
| Task lists | ✅ (with pymdownx.tasklist) | ✅ (with ext) | ✅ (with plugin) | ✅ (with `.tasklist`) | ✅ (optional) | ✅ (with `.tasklist`) |
| Strikethrough | ✅ (with pymdownx.tilde) | ✅ (with ext) | ✅ (with plugin) | ✅ (with `.strikethrough`) | ✅ (optional) | ✅ (with GFM or `.strikethrough`) |
| Autolinks | ✅ (with pymdownx.magiclink) | ❌ | ✅ (with plugin) | ✅ (with `.autolink`) | ✅ (with GFM) | ✅ (with `.autolink_ext`) |
| GFM Alerts | ❌ | ❌ | ❌ | ✅ (with `.alerts`) | ✅ (with GFM) | ❌ |
| **Extended Features** |||||||
| Footnotes | ✅ (with ext) | ✅ (with ext) | ✅ (with plugin) | ✅ (with `.footnotes`) | ✅ (optional) | ✅ (with `.footnote`) |
| Definition lists | ✅ (with ext) | ✅ (with ext) | ❌ | ✅ (with `.description_lists`) | ✅ (optional) | ✅ (with `.deflist`) |
| Admonitions | ✅ (with ext) | ❌ | ❌ | ❌ | ❌ | ❌ |
| Math notation | ✅ (with pymdownx.arithmatex) | ❌ | ✅ (with plugin) | ✅ (with `.math_dollars`/`.math_code`) | ✅ (optional) | ❌ |
| Superscript | ✅ (with ext) | ❌ | ❌ | ✅ (with `.superscript`) | ✅ (optional) | ❌ |
| Subscript | ✅ (with ext) | ❌ | ❌ | ✅ (with `.subscript`) | ✅ (optional) | ❌ |
| Table of Contents | ✅ (with ext) | ✅ (with ext) | ❌ | ❌ | ❌ | ❌ |
| Front matter | ✅ (with ext) | ✅ (with ext) | ❌ | ✅ (with `.front_matter_delimiter`) | ✅ (optional) | ✅ (with `.front_matter`) |
| Wikilinks | ✅ (with ext) | ❌ | ❌ | ✅ (with `.wikilinks_*`) | ✅ (optional) | ❌ |
| Header IDs | ✅ (with ext) | ✅ (with ext) | ❌ | ✅ (with `.header_ids`) | ✅ (optional) | ✅ (with `.heading_anchors`) |
| Multiline blockquotes | ❌ | ❌ | ❌ | ✅ (with `.multiline_block_quotes`) | ❌ | ❌ |
| Syntax highlighting | ✅ (with ext) | ✅ (with ext) | ✅ (with plugin) | ✅ (with plugins) | ❌ | ❌ |
| Special features | Admonitions | Smart quotes | Custom renderers | Spoiler, Greentext | Definition lists | Tree structure, very fast (20x faster than Python-Markdown) |
