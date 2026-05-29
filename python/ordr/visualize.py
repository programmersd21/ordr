"""Terminal-based sorting visualization."""

import time
from collections.abc import Generator

from rich.console import Console
from rich.live import Live
from rich.panel import Panel

console = Console()


def visualize_bubble(arr: list[int]) -> Generator[tuple[list[int], int, int], None, None]:
    arr = arr.copy()
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
                yield (arr.copy(), j, j + 1)
        if not swapped:
            break
    yield (arr, -1, -1)


def visualize_insertion(arr: list[int]) -> Generator[tuple[list[int], int, int], None, None]:
    arr = arr.copy()
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            yield (arr.copy(), j, j + 1)
            j -= 1
        arr[j + 1] = key
        yield (arr.copy(), j + 1, i)
    yield (arr, -1, -1)


def visualize_quick(arr: list[int]) -> Generator[tuple[list[int], int, int], None, None]:
    arr = arr.copy()

    def partition(low: int, high: int) -> Generator[tuple[list[int], int, int], None, int]:
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                yield (arr.copy(), i, j)
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        yield (arr.copy(), i + 1, high)
        return i + 1

    def quicksort(low: int, high: int) -> Generator[tuple[list[int], int, int], None, None]:
        if low < high:
            pi = yield from partition(low, high)
            yield from quicksort(low, pi - 1)
            yield from quicksort(pi + 1, high)

    yield from quicksort(0, len(arr) - 1)
    yield (arr, -1, -1)


def visualize_merge(arr: list[int]) -> Generator[tuple[list[int], int, int], None, None]:
    """Merge sort with visualization steps."""
    arr = arr.copy()

    def merge(left: int, mid: int, right: int) -> Generator[tuple[list[int], int, int], None, None]:
        left_part = arr[left : mid + 1]
        right_part = arr[mid + 1 : right + 1]

        i = j = 0
        k = left

        while i < len(left_part) and j < len(right_part):
            if left_part[i] <= right_part[j]:
                arr[k] = left_part[i]
                i += 1
            else:
                arr[k] = right_part[j]
                j += 1
            yield (arr.copy(), k, k)
            k += 1

        while i < len(left_part):
            arr[k] = left_part[i]
            yield (arr.copy(), k, k)
            i += 1
            k += 1

        while j < len(right_part):
            arr[k] = right_part[j]
            yield (arr.copy(), k, k)
            j += 1
            k += 1

    def merge_sort(left: int, right: int) -> Generator[tuple[list[int], int, int], None, None]:
        if left < right:
            mid = (left + right) // 2
            yield from merge_sort(left, mid)
            yield from merge_sort(mid + 1, right)
            yield from merge(left, mid, right)

    yield from merge_sort(0, len(arr) - 1)
    yield (arr, -1, -1)


def render_array(arr: list[int], highlight1: int = -1, highlight2: int = -1) -> str:
    """Render array as ASCII bars."""
    if not arr:
        return ""

    max_val = max(arr)
    min_val = min(arr)
    range_val = max_val - min_val if max_val != min_val else 1

    lines = []
    max_height = 20

    for height in range(max_height, 0, -1):
        line = ""
        for i, val in enumerate(arr):
            normalized = int(((val - min_val) / range_val) * max_height)
            if normalized >= height:
                if i == highlight1 or i == highlight2:
                    line += "[red]█[/red]"
                else:
                    line += "[cyan]█[/cyan]"
            else:
                line += " "
        lines.append(line)

    return "\n".join(lines)


def visualize(arr: list[int], algorithm: str = "bubble", delay: float = 0.05) -> None:
    """
    Visualize sorting algorithm in terminal.

    Args:
        arr: Array to sort
        algorithm: Algorithm name ('bubble', 'insertion', 'quick', 'merge')
        delay: Delay between frames in seconds
    """
    algorithms = {
        "bubble": visualize_bubble,
        "insertion": visualize_insertion,
        "quick": visualize_quick,
        "merge": visualize_merge,
    }

    if algorithm not in algorithms:
        raise ValueError(f"Unknown algorithm: {algorithm}. Choose from {list(algorithms.keys())}")

    if len(arr) > 50:
        console.print("[yellow]Warning: Large arrays may be slow to visualize[/yellow]")

    generator = algorithms[algorithm](arr)

    with Live(console=console, refresh_per_second=20) as live:
        for state, h1, h2 in generator:
            rendered = render_array(state, h1, h2)
            panel = Panel(
                rendered, title=f"[bold]{algorithm.capitalize()} Sort[/bold]", border_style="blue"
            )
            live.update(panel)
            time.sleep(delay)

    console.print("[green]Sorting complete![/green]")
