# Visualization API

Terminal-based sorting visualization.

## visualize()

```python
visualize(
    arr: list[int],
    algorithm: str = "bubble",
    delay: float = 0.05
) -> None
```

Visualize a sorting algorithm in the terminal.

**Parameters:**
- `arr`: Array to sort
- `algorithm`: Algorithm name (`"bubble"`, `"insertion"`, `"quick"`, `"merge"`)
- `delay`: Delay between frames in seconds

**Example:**

```python
from ordr.visualize import visualize

arr = [5, 2, 8, 1, 9, 3, 7, 4, 6]
visualize(arr, algorithm="bubble", delay=0.1)
```

## Supported Algorithms

- `bubble` - Bubble sort
- `insertion` - Insertion sort
- `quick` - Quicksort
- `merge` - Merge sort

## Notes

- Visualization uses Python implementations (not Rust) for step-by-step rendering
- Recommended array size: 10-30 elements
- Larger arrays may be slow to visualize
- Uses Rich library for terminal rendering

## CLI Usage

```bash
# Visualize bubble sort
ordr viz --algorithm bubble --size 20

# Visualize quicksort with custom delay
ordr viz --algorithm quick --size 25 --delay 0.05
```
