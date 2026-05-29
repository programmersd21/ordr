# ordr

**High-performance adaptive sorting for Python, powered by Rust.**

ordr is a professional sorting library that combines the performance of Rust with the ergonomics of Python. It features adaptive algorithm selection, parallel sorting, and comprehensive benchmarking tools.

## Features

- **Rust-Powered Performance** - Core algorithms in Rust with branchless partitioning, prefetching, and LTO
- **Adaptive Algorithm Selection** - Automatically chooses the best algorithm for your data based on size, presortedness, duplicates, and value range
- **Parallel Sorting** - Leverage multiple cores for large datasets
- **NumPy Integration** - Accepts numpy arrays with zero-copy in-place sorting
- **Rich Algorithm Suite** - PDQSort, IntroSort, TimSort, Radix, and more
- **Comprehensive Benchmarking** - Built-in tools to measure and compare performance
- **Terminal Visualization** - Watch sorting algorithms in action
- **Full Type Safety** - PEP 561 compliant with comprehensive type stubs for IDEs

## Quick Start

### Installation

```bash
pip install ordr-python
```

### Basic Usage

```python
import ordr

# Smart adaptive sort (recommended)
arr = [3, 1, 4, 1, 5, 9, 2, 6]
sorted_arr = ordr.smart(arr)

# Use specific algorithms
ordr.pdq(arr)                # Pattern-Defeating QuickSort
ordr.tim(arr)                # TimSort (stable)
ordr.intro(arr)              # IntroSort
ordr.radix(arr)              # Radix sort
ordr.par_sort(arr)           # Parallel stable sort
ordr.par_sort_unstable(arr)  # Parallel unstable sort
```

### Benchmarking

```python
from ordr.benchmark import compare, display_comparison

results = compare(size=10000, pattern="random")
display_comparison(results)
```

### CLI

```bash
# Show information
ordr info

# Run benchmarks
ordr bench --size 10000 --pattern random

# Visualize sorting
ordr viz --algorithm bubble --size 20
```

## Why ordr?

### Performance

ordr's Rust core delivers performance that rivals or exceeds native implementations:

- **Smart dispatch** analyzes your data and selects the optimal algorithm
- **Optimized allocator** reduces allocation overhead
- **Branchless partition** minimizes branch misprediction penalties
- **Parallel execution** for large datasets

### Ergonomics

Despite its performance focus, ordr maintains a clean, Pythonic API:

```python
# Simple and intuitive
sorted_data = ordr.smart(data)

# Explicit when needed
sorted_data = ordr.pdq(data)
```

### Observability

Built-in benchmarking and visualization help you understand performance:

```bash
ordr bench --pattern nearly_sorted
ordr viz --algorithm quick
```

## Algorithm Overview

| Algorithm | Time Complexity | Space | Stable | Best For |
|-----------|----------------|-------|--------|----------|
| **smart** | Adaptive | Varies | Varies | General use (recommended) |
| **pdq** | O(n log n) | O(log n) | No | Random data |
| **intro** | O(n log n) | O(log n) | No | General purpose |
| **tim** | O(n log n) | O(n) | Yes | Nearly sorted, real-world data |
| **radix** | O(nk) | O(n) | Yes | Integer arrays |
| **par_sort** | O(n log n) | O(n) | Yes | Large datasets |
| **par_sort_unstable** | O(n log n) | O(log n) | No | Large datasets (fastest) |

## Next Steps

- [Getting Started](getting-started.md) - Detailed installation and usage guide
- [API Reference](api/algorithms.md) - Complete API documentation
- [Choosing an Algorithm](guides/choosing-an-algorithm.md) - Algorithm selection guide
- [Benchmarking Guide](guides/benchmarking.md) - Performance measurement
- [Architecture](internals/architecture.md) - How ordr works internally

## Contributing

We welcome contributions! See [CONTRIBUTING.md](https://github.com/programmersd21/ordr/blob/main/CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](https://github.com/programmersd21/ordr/blob/main/LICENSE) for details.
