"""Command-line interface for ordr."""

import random

import typer
from rich.console import Console
from rich.panel import Panel

from ordr.benchmark import compare, display_comparison, profile
from ordr.visualize import visualize

app = typer.Typer(help="ordr: High-performance adaptive sorting for Python")
console = Console()


@app.command()
def info():
    """Display information about ordr."""
    info_text = """
[bold cyan]ordr[/bold cyan] - High-performance adaptive sorting for Python, powered by Rust

[bold]Available Algorithms:[/bold]
  smart, pdq, intro, tim, quick, merge, heap, radix, par_sort, insertion, bubble

[bold]Features:[/bold]
  - Rust-powered performance
  - Adaptive algorithm selection
  - Parallel sorting support
  - Comprehensive benchmarking
  - Terminal visualization
"""
    console.print(Panel(info_text, border_style="cyan"))


@app.command()
def bench(
    size: int = typer.Option(10000, help="Array size"),
    pattern: str = typer.Option(
        "random", help="Data pattern (random/sorted/reverse/nearly_sorted/duplicates)"
    ),
    algorithms: str = typer.Option("", help="Comma-separated algorithm names (empty = all)"),
):
    """Run sorting benchmarks."""
    console.print(f"\n[bold]Benchmarking on {pattern} data (size={size:,})[/bold]\n")

    algo_list = [a.strip() for a in algorithms.split(",")] if algorithms else None

    try:
        results = compare(size=size, pattern=pattern, algorithms=algo_list)
        display_comparison(results)
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def prof(
    algorithm: str = typer.Option("smart", help="Algorithm to profile"),
    pattern: str = typer.Option("random", help="Data pattern"),
    sizes: str = typer.Option("1000,10000,100000", help="Comma-separated sizes"),
):
    """Profile an algorithm across different sizes."""
    size_list = [int(s.strip()) for s in sizes.split(",")]

    console.print(f"\n[bold]Profiling {algorithm} on {pattern} data[/bold]\n")

    try:
        profile(sizes=size_list, pattern=pattern, algorithm=algorithm)
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def viz(
    algorithm: str = typer.Option(
        "bubble", help="Algorithm to visualize (bubble/insertion/quick/merge)"
    ),
    size: int = typer.Option(20, help="Array size (recommended: 10-30)"),
    delay: float = typer.Option(0.05, help="Delay between frames (seconds)"),
):
    """Visualize a sorting algorithm."""
    if size > 50:
        console.print("[yellow]Warning: Large arrays may be slow. Recommended size: 10-30[/yellow]")

    arr = list(range(1, size + 1))
    random.shuffle(arr)

    console.print(f"\n[bold]Visualizing {algorithm} sort[/bold]")
    console.print(f"Array size: {size}\n")

    try:
        visualize(arr, algorithm=algorithm, delay=delay)
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
