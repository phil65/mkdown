from __future__ import annotations

import json
from pathlib import Path
from typing import Any, ClassVar


class MarkdownConverter:
    """An extended wrapper class for markdown to HTML conversion libraries.

    Supports multiple markdown flavors, caching, sanitization, and custom extensions.
    """

    SUPPORTED_ENGINES: ClassVar = [
        "python-markdown",
        "mistune",
        "markdown2",
        "markdownify",
        "mdx_math",
    ]

    # Cache for converter instances
    _converter_cache: ClassVar[dict[str, Any]] = {}

    def __init__(
        self,
        engine: str = "python-markdown",
        cache_enabled: bool = True,
    ):
        """Initialize the markdown converter.

        Args:
            engine (str): The markdown engine to use
            cache_enabled (bool): Whether to cache converter instances
        """
        if engine not in self.SUPPORTED_ENGINES:
            msg = f"Unsupported engine. Choose from: {self.SUPPORTED_ENGINES}"
            raise ValueError(msg)

        self.engine = engine
        self.cache_enabled = cache_enabled
        self._setup_engine()

    def _get_cache_key(self, extensions: list[str] | None, **kwargs: Any) -> str:
        """Generate a cache key based on configuration."""
        cache_data = {
            "engine": self.engine,
            "extensions": sorted(extensions) if extensions else None,
            **kwargs,
        }
        return json.dumps(cache_data, sort_keys=True)

    def _get_cached_converter(self, cache_key: str):
        """Get or create a cached converter instance."""
        return self._converter_cache.get(cache_key)

    def _setup_engine(self):
        """Set up the chosen markdown engine with default configurations."""
        if self.engine == "python-markdown":
            import markdown

            self.converter = markdown.Markdown(extensions=["extra"])
        elif self.engine == "mistune":
            import mistune

            self.converter = mistune.create_markdown()
        elif self.engine == "markdown2":
            import markdown2

            self.converter = markdown2.Markdown()

    def load_custom_extension(self, extension_path: str | Path) -> Any:
        """Load a custom markdown extension from a Python file."""
        extension_path = Path(extension_path)
        if not extension_path.exists():
            msg = f"Extension file not found: {extension_path}"
            raise FileNotFoundError(msg)

        import importlib.util

        spec = importlib.util.spec_from_file_location(extension_path.stem, extension_path)
        # Check if spec is None
        if spec is None:
            msg = f"Could not load extension spec from {extension_path}"
            raise ImportError(msg)

        # Check if loader is None
        if spec.loader is None:
            msg = f"No loader available for extension {extension_path}"
            raise ImportError(msg)

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.Extension

    def convert(
        self,
        text: str,
        extensions: list[str] | None = None,
        admonitions: bool = False,
        custom_extensions: list[str | Path] | None = None,
        sanitize_options: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> str:
        """Convert markdown text to HTML with extended options.

        Args:
            text: The markdown text to convert
            extensions: List of extensions to use
            admonitions: Whether to enable admonitions
            custom_extensions: List of paths to custom extensions
            sanitize_options: Options for HTML sanitization
            **kwargs: Additional engine-specific options

        Returns:
            The converted HTML text
        """
        # Load custom extensions if provided
        if custom_extensions:
            loaded_extensions = [
                self.load_custom_extension(ext) for ext in custom_extensions
            ]
            if extensions:
                extensions.extend(loaded_extensions)
            else:
                extensions = loaded_extensions

        # Get cached converter or create new one
        if self.cache_enabled:
            cache_key = self._get_cache_key(extensions, **kwargs)
            converter = self._get_cached_converter(cache_key)
            if converter:
                html_content = converter.convert(text)
            else:
                html_content = self._convert_with_engine(
                    text, extensions, admonitions, **kwargs
                )
                self._converter_cache[cache_key] = self.converter
        else:
            html_content = self._convert_with_engine(
                text, extensions, admonitions, **kwargs
            )

        return html_content

    def _convert_with_engine(
        self,
        text: str,
        extensions: list[str] | None,
        admonitions: bool,
        **kwargs: Any,
    ) -> str:
        """Handle conversion with specific engine."""
        if self.engine == "python-markdown":
            return self._convert_python_markdown(text, extensions, admonitions, **kwargs)
        if self.engine == "mistune":
            return self._convert_mistune(text, **kwargs)
        if self.engine == "markdown2":
            return self._convert_markdown2(text, extensions, admonitions, **kwargs)

        msg = f"Unsupported engine: {self.engine}"
        raise ValueError(msg)

    def _convert_python_markdown(
        self,
        text: str,
        extensions: list[str] | None,
        admonitions: bool,
        **kwargs: Any,
    ) -> str:
        """Convert markdown using python-markdown."""
        import markdown

        # Prepare extensions list
        md_extensions = extensions or []

        # Add admonition extension if requested
        if admonitions and "admonition" not in md_extensions:
            md_extensions.append("admonition")

        # Configure converter
        if self.engine == "python-markdown":
            self.converter = markdown.Markdown(extensions=md_extensions)
            return self.converter.convert(text)

        return ""

    def _convert_mistune(self, text: str, **kwargs: Any) -> str:
        """Convert markdown using mistune."""
        if self.engine == "mistune":
            import mistune

            self.converter = mistune.create_markdown(**kwargs)
            return self.converter(text)

        return ""

    def _convert_markdown2(
        self, text: str, extensions: list[str] | None, admonitions: bool, **kwargs: Any
    ) -> str:
        """Convert markdown using markdown2."""
        if self.engine == "markdown2":
            import markdown2

            extras = kwargs.pop("extras", [])
            if extensions:
                extras.extend(extensions)
            if admonitions:
                extras.append("admonition")

            self.converter = markdown2.Markdown(extras=extras, **kwargs)
            return self.converter.convert(text)

        return ""

    @staticmethod
    def get_supported_extensions(engine: str) -> list[str]:
        """Get list of supported extensions for the specified engine."""
        import markdown
        import markdown2

        extension_map = {
            "python-markdown": markdown.util.get_installed_extensions(),
            "markdown2": markdown2.DEFAULT_EXTRAS,
            "mistune": ["tables", "footnotes", "strikethrough", "task_lists"],
        }
        return extension_map.get(engine, [])
