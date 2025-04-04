"""Benchmarking module for comparing markdown parser performance."""

from __future__ import annotations

from pathlib import Path
import sys
import time
from typing import TYPE_CHECKING, Any

from mkdown.parsers.parser import MarkdownParser


if TYPE_CHECKING:
    from collections.abc import Callable


def load_test_cases(cases_dir: Path | str) -> dict[str, str]:
    """Load all test case files from the specified directory.

    Args:
        cases_dir: Directory containing test cases

    Returns:
        Dictionary mapping case names to their content
    """
    cases_dir = Path(cases_dir)
    test_cases = {}

    for file_path in cases_dir.glob("*.txt"):
        with file_path.open(encoding="utf-8") as f:
            content = f.read()
            test_cases[file_path.stem] = content

    return test_cases


def run_benchmark(
    parser_func: Callable[[str], str], content: str, iterations: int = 50
) -> float:
    """Run benchmark for a specific parser function.

    Args:
        parser_func: Parser function to benchmark
        content: Markdown content to parse
        iterations: Number of iterations to run

    Returns:
        Average execution time in milliseconds
    """
    # Warm up
    parser_func(content)

    start_time = time.time()
    for _ in range(iterations):
        parser_func(content)
    duration = time.time() - start_time

    # Return average time in milliseconds
    return (duration * 1000) / iterations


def benchmark_parsers(
    test_cases: dict[str, str], iterations: int = 50
) -> dict[str, dict[str, float]]:
    """Benchmark all parsers against all test cases.

    Args:
        test_cases: Dictionary mapping case names to their content
        iterations: Number of iterations for each benchmark

    Returns:
        Dictionary with benchmark results
    """
    results: dict[str, Any] = {}

    # Create parser configurations to test
    parsers = {
        "comrak (default)": lambda text: MarkdownParser(
            rust_parser="comrak", use_lxml=True
        ).convert(text),
        "comrak (unsafe)": lambda text: MarkdownParser(
            rust_parser="comrak", use_lxml=True, unsafe=True
        ).convert(text),
        "comrak (no lxml)": lambda text: MarkdownParser(
            rust_parser="comrak", use_lxml=False
        ).convert(text),
        # Add pyromark if available
        "pyromark": lambda text: MarkdownParser(
            rust_parser="pyromark", use_lxml=True
        ).convert(text),
    }

    import markdown

    parsers["python-markdown"] = markdown.markdown

    for case_name, content in test_cases.items():
        results[case_name] = {}

        for parser_name, parser_func in parsers.items():
            try:
                avg_time = run_benchmark(parser_func, content, iterations)
                results[case_name][parser_name] = avg_time
                print(f"{parser_name} - {case_name}: {avg_time:.2f}ms")
            except Exception as e:  # noqa: BLE001
                print(f"Error benchmarking {parser_name} on {case_name}: {e}")
                results[case_name][parser_name] = float("nan")

    return results


def print_summary(results: dict[str, dict[str, float]]) -> None:
    """Print a summary of benchmark results.

    Args:
        results: Dictionary with benchmark results
    """
    parser_names: set[str] = set()
    for case_results in results.values():
        parser_names.update(case_results.keys())

    # Calculate averages across all test cases
    parser_list = sorted(parser_names)
    averages = dict.fromkeys(parser_list, 0.0)
    counts = dict.fromkeys(parser_list, 0)

    for case_results in results.values():
        for parser, time_ in case_results.items():
            averages[parser] += time_
            counts[parser] += 1

    for parser in parser_names:
        if counts[parser] > 0:
            averages[parser] /= counts[parser]

    print("\nSUMMARY")
    print("=" * 60)
    print(f"{'Parser':<20} | {'Average Time (ms)':<15} | {'Relative':<10}")
    print("-" * 60)

    min_avg = min(avg for avg in averages.values() if avg > 0)
    for parser in parser_names:
        if counts[parser] > 0:
            relative = averages[parser] / min_avg if min_avg > 0 else 0
            print(f"{parser:<20} | {averages[parser]:<15.4f} | {relative:<10.4f}x")

    print("=" * 60)


def main() -> None:
    """Run benchmarks with command line arguments."""
    # Determine benchmark directory
    script_dir = Path(__file__).parent
    cases_dir = script_dir / "cases"

    # Allow command line arguments to specify test cases
    specific_cases = sys.argv[1:] if len(sys.argv) > 1 else None

    # Load test cases
    all_test_cases = load_test_cases(cases_dir)

    # Filter test cases if specific ones were requested
    if specific_cases:
        test_cases = {
            name: content
            for name, content in all_test_cases.items()
            if name in specific_cases
        }
    else:
        test_cases = all_test_cases

    # Run benchmarks
    iterations = 20  # Lower default to speed up full benchmarks
    results = benchmark_parsers(test_cases, iterations)

    # Print summary
    print_summary(results)


if __name__ == "__main__":
    main()
