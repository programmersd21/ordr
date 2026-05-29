"""Benchmarking utilities for ordr."""

import random
import time
from collections.abc import Callable
from typing import Any

from rich.console import Console
from rich.table import Table

import ordr

console = Console()


def generate_random(size: int) -> list[int]:
    return [random.randint(-1000000, 1000000) for _ in range(size)]


def generate_sorted(size: int) -> list[int]:
    return list(range(size))


def generate_reverse(size: int) -> list[int]:
    return list(range(size, 0, -1))


def generate_nearly_sorted(size: int) -> list[int]:
    arr = list(range(size))
    swaps = size // 10
    for _ in range(swaps):
        i, j = random.randint(0, size - 1), random.randint(0, size - 1)
        arr[i], arr[j] = arr[j], arr[i]
    return arr


def generate_duplicates(size: int) -> list[int]:
    return [random.randint(0, size // 10) for _ in range(size)]


def benchmark_function(func: Callable[[Any], Any], arr: list[int], runs: int = 5) -> float:
    """Benchmark function and return median time in ms."""
    times = []
    for _ in range(runs):
        arr_copy = arr.copy()
        start = time.perf_counter()
        func(arr_copy)
        end = time.perf_counter()
        times.append((end - start) * 1000)
    return sorted(times)[len(times) // 2]


def compare(
    size: int = 10000, pattern: str = "random", algorithms: list[str] | None = None
) -> dict[str, float]:
    """Compare sorting algorithms on specific data pattern."""
    generators: dict[str, Callable[[int], list[int]]] = {
        "random": generate_random,
        "sorted": generate_sorted,
        "reverse": generate_reverse,
        "nearly_sorted": generate_nearly_sorted,
        "duplicates": generate_duplicates,
    }

    if pattern not in generators:
        raise ValueError(f"Unknown pattern: {pattern}")

    arr = generators[pattern](size)

    all_algorithms: dict[str, Callable[[Any], Any]] = {
        "smart": ordr.smart,
        "pdq": ordr.pdq,
        "intro": ordr.intro,
        "tim": ordr.tim,
        "quick": ordr.quick,
        "merge": ordr.merge,
        "heap": ordr.heap,
        "radix": ordr.radix,
        "par_sort": ordr.par_sort,
        "builtin": sorted,
    }

    if algorithms:
        test_algorithms = {k: v for k, v in all_algorithms.items() if k in algorithms}
    else:
        test_algorithms = all_algorithms

    return {name: benchmark_function(func, arr) for name, func in test_algorithms.items()}


def profile(
    sizes: list[int] = [1000, 10000, 100000], pattern: str = "random", algorithm: str = "smart"
) -> None:
    """
    Profile an algorithm across different input sizes.

    Args:
        sizes: List of array sizes to test
        pattern: Data pattern
        algorithm: Algorithm name
    """
    algorithms_map: dict[str, Callable[[Any], Any]] = {
        "smart": ordr.smart,
        "pdq": ordr.pdq,
        "intro": ordr.intro,
        "tim": ordr.tim,
        "quick": ordr.quick,
        "merge": ordr.merge,
        "heap": ordr.heap,
        "radix": ordr.radix,
        "par_sort": ordr.par_sort,
        "builtin": sorted,
    }

    if algorithm not in algorithms_map:
        raise ValueError(f"Unknown algorithm: {algorithm}")

    func = algorithms_map[algorithm]

    table = Table(title=f"Profile: {algorithm} on {pattern} data")
    table.add_column("Size", style="cyan")
    table.add_column("Time (ms)", style="magenta")
    table.add_column("Time per element (us)", style="green")

    for size in sizes:
        generators: dict[str, Callable[[int], list[int]]] = {
            "random": generate_random,
            "sorted": generate_sorted,
            "reverse": generate_reverse,
            "nearly_sorted": generate_nearly_sorted,
            "duplicates": generate_duplicates,
        }
        arr = generators[pattern](size)
        time_ms = benchmark_function(func, arr)
        time_per_elem = (time_ms * 1000) / size

        table.add_row(f"{size:,}", f"{time_ms:.2f}", f"{time_per_elem:.3f}")

    console.print(table)


def display_comparison(results: dict[str, float], baseline: str = "builtin") -> None:
    """Display benchmark results in a rich table."""
    table = Table(title="Sorting Algorithm Comparison")
    table.add_column("Algorithm", style="cyan")
    table.add_column("Time (ms)", style="magenta")
    table.add_column("vs Baseline", style="green")

    baseline_time = results.get(baseline, 0.0)

    sorted_results = sorted(results.items(), key=lambda x: x[1])

    for name, time_ms in sorted_results:
        if baseline_time > 0 and name != baseline:
            ratio = time_ms / baseline_time
            vs_baseline = f"{ratio:.2f}x"
            if ratio < 1.0:
                vs_baseline = f"[green]{ratio:.2f}x faster[/green]"
            elif ratio > 1.0:
                vs_baseline = f"[red]{ratio:.2f}x slower[/red]"
        else:
            vs_baseline = "baseline"

        table.add_row(name, f"{time_ms:.2f}", vs_baseline)

    console.print(table)
