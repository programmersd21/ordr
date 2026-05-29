# Getting Started

## Installation

### From PyPI

```bash
pip install ordr-py
```

### From Source

```bash
git clone https://github.com/programmersd21/ordr.git
cd ordr
python build_lib.py
```

## Development Scripts

- **Build Library**: `python build_lib.py` builds the Rust extension in release mode and outputs wheels to `build/`.
- **Lint and Format**: `python lint.py` runs Ruff, Mypy, cargo fmt, cargo clippy, and pytest.
- **Benchmark**: `python bench_hyperfine.py <algo> <size> <pattern>` runs a single algorithm benchmark for use with hyperfine.
- **Test Examples**: `python run_examples.py` executes all scripts in the `examples/` directory.
- **Rust/Python Tests**: Use `cargo test` and `pytest` for standard unit testing.

### Requirements

- Python 3.10 or later
- Rust 1.70 or later (for building from source)

## Basic Usage

### Your First Sort

```python
import ordr

arr = [3, 1, 4, 1, 5, 9, 2, 6]
sorted_arr = ordr.smart(arr)
print(sorted_arr)  # [1, 1, 2, 3, 4, 5, 6, 9]
```

### Choosing an Algorithm

```python
import ordr

arr = [3, 1, 4, 1, 5, 9, 2, 6]

# Adaptive (recommended)
ordr.smart(arr)

# Fast general-purpose
ordr.pdq(arr)

# Stable sort
ordr.tim(arr)

# Guaranteed O(n log n)
ordr.intro(arr)

# Integer-optimized
ordr.radix(arr)

# Parallel
ordr.par_sort(arr)
ordr.par_sort_unstable(arr)
```

### NumPy Arrays

```python
import numpy as np
import ordr

arr = np.array([3, 1, 4, 1, 5], dtype=np.int64)
ordr.smart(arr)  # Sorts in-place (zero-copy)
print(arr)       # [1, 1, 3, 4, 5]
```

## Benchmarking

### Compare Algorithms

```python
from ordr.benchmark import compare, display_comparison

results = compare(
    size=10000,
    pattern="random",
    algorithms=["smart", "pdq", "tim", "builtin"]
)
display_comparison(results)
```

### Profile Across Sizes

```python
from ordr.benchmark import profile

profile(
    sizes=[1000, 10000, 100000],
    pattern="random",
    algorithm="smart"
)
```

## Visualization

### Terminal Visualization

```python
from ordr.visualize import visualize

arr = [5, 2, 8, 1, 9, 3, 7, 4, 6]
visualize(arr, algorithm="bubble", delay=0.1)
```

### Using the CLI

```bash
# Visualize bubble sort
ordr viz --algorithm bubble --size 20

# Visualize quicksort
ordr viz --algorithm quick --size 25 --delay 0.05
```

## CLI Usage

### Show Information

```bash
ordr info
```

### Run Benchmarks

```bash
# Basic benchmark
ordr bench

# Custom size and pattern
ordr bench --size 50000 --pattern nearly_sorted

# Specific algorithms
ordr bench --algorithms "smart,pdq,tim"
```

### Profile Algorithm

```bash
ordr prof --algorithm smart --sizes "1000,10000,100000"
```

### Hyperfine Benchmarks

```bash
# Install hyperfine
cargo install hyperfine

# Run benchmark
hyperfine --warmup 3 "python bench_hyperfine.py smart 100000 random"
```

## Common Patterns

### Large Datasets

For large datasets, use parallel sorting:

```python
large_data = list(range(1000000, 0, -1))
sorted_data = ordr.par_sort_unstable(large_data)
```

### Nearly Sorted Data

For nearly sorted data, TimSort excels:

```python
nearly_sorted = list(range(10000))
# Swap a few elements
nearly_sorted[100], nearly_sorted[101] = nearly_sorted[101], nearly_sorted[100]

# Smart sort will detect this and use TimSort
result = ordr.smart(nearly_sorted)
```

## Next Steps

- [API Reference](api/algorithms.md) - Detailed API documentation
- [Choosing an Algorithm](guides/choosing-an-algorithm.md) - Algorithm selection guide
- [Benchmarking Guide](guides/benchmarking.md) - Advanced benchmarking
- [Architecture](internals/architecture.md) - How ordr works
