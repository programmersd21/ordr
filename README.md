# ordr

[![CI](https://img.shields.io/github/actions/workflow/status/programmersd21/ordr/ci.yml?style=for-the-badge&logo=github&label=CI)](https://github.com/programmersd21/ordr/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Rust](https://img.shields.io/badge/rust-1.70%2B-orange?style=for-the-badge&logo=rust&logoColor=white)](https://www.rust-lang.org/)
[![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)](https://opensource.org/licenses/MIT)

> **High-performance adaptive sorting for Python, powered by Rust.**

`ordr` is a professional sorting library that bridges the gap between Python's ergonomics and Rust's raw performance. It features a suite of optimized sorting algorithms and an intelligent adaptive dispatch engine that selects the best strategy for your data.

## Key Features

- **Adaptive Dispatch (`ordr.smart`)**: Automatically chooses the best algorithm by inspecting data characteristics (size, presortedness, duplicate ratio, value range).
- **High Performance**: Core algorithms implemented in Rust with heavy optimizations (branchless partition, prefetching, LTO).
- **Parallel Sorting**: Leverages Rayon for multi-threaded sorting of massive datasets.
- **NumPy Integration**: Accepts numpy arrays directly with zero-copy in-place sorting.
- **Modern Algorithms**: Includes PDQSort (Pattern-Defeating Quicksort), TimSort, IntroSort, Radix Sort, and sorting networks for small arrays.
- **Developer Tools**: Built-in benchmarking suite, terminal-based sorting visualizer, and hyperfine benchmarking scripts.

## Installation

```bash
pip install ordr-python
```

*(Note: Requires a Rust compiler for source builds. Pre-built wheels coming soon.)*

## Usage

### Basic Sorting

```python
import ordr
import random

data = [random.randint(0, 1000) for _ in range(10000)]

# Use the adaptive smart sort (recommended)
sorted_data = ordr.smart(data)

# Or choose a specific algorithm
sorted_data = ordr.pdq(data)             # Pattern-Defeating Quicksort
sorted_data = ordr.tim(data)             # TimSort (stable)
sorted_data = ordr.par_sort(data)        # Parallel stable sort
sorted_data = ordr.par_sort_unstable(data) # Parallel unstable sort
sorted_data = ordr.radix(data)           # Radix sort for integers
```

### NumPy Support

```python
import numpy as np
import ordr

arr = np.array([3, 1, 4, 1, 5], dtype=np.int64)
ordr.smart(arr)  # Sorts in-place, zero-copy
print(arr)       # [1, 1, 3, 4, 5]
```

### Development Scripts

The repository includes several utility scripts for common development tasks:

- **Build**: `python build_lib.py` builds the Rust extension and creates wheels in the `build/` directory.
- **Lint**: `python lint.py` runs Ruff (formatting and linting), Mypy, cargo fmt, cargo clippy, and pytest.
- **Benchmarks**: `make bench algo=<algo> size=<N> pattern=<pattern>` runs hyperfine for a single algorithm. Low-level: `python bench_hyperfine.py generate <size> <pattern> <outfile>` to prepare data, then `python bench_hyperfine.py run <algo> <datafile>` to time.
- **Examples**: `python run_examples.py` runs all scripts in the `examples/` directory.

### Benchmarking

`ordr` comes with a first-class benchmarking suite to compare performance against Python's built-in `sorted()`.

```python
from ordr.benchmark import compare, display_comparison

# Compare ordr.smart against Python's sorted()
results = compare(size=10000, pattern="random")
display_comparison(results)
```

Run `make bench-compare` to generate a hyperfine report in `benches/report.md`.

Performance on **1,000,000 random integers** (in-process timing):

| Algorithm | Time | vs builtin |
| :--- | :--- | :--- |
| `smart` | 63 ms | **4.2x faster** |
| `par_sort` | 66 ms | **4.0x faster** |
| `radix` | 100 ms | **2.7x faster** |
| `pdq` | 160 ms | **1.7x faster** |
| `builtin` | 267 ms | 1.0x (baseline) |

## Algorithm Complexity

| Algorithm | Best | Average | Worst | Space | Stable |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`ordr.smart`** | O(n) | O(n log n) | O(n log n) | Varies | Varies* |
| **`ordr.pdq`** | O(n) | O(n log n) | O(n log n) | O(log n) | No |
| **`ordr.tim`** | O(n) | O(n log n) | O(n log n) | O(n) | Yes |
| **`ordr.intro`** | O(n log n) | O(n log n) | O(n log n) | O(log n) | No |
| **`ordr.radix`** | O(nk) | O(nk) | O(nk) | O(n+k) | Yes |
| **`ordr.par_sort`** | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes |
| **`ordr.par_sort_unstable`** | O(n log n) | O(n log n) | O(n log n) | O(log n) | No |

*\*`ordr.smart` may choose a stable or unstable algorithm depending on the data.*

## Architecture

`ordr` is built with a modular architecture that separates the high-performance Rust core from the ergonomic Python API.

- **Rust Core**: Found in `src/`, containing the implementation of all sorting algorithms and the analysis engine.
- **Adaptive Engine**: Located in `src/adaptive/`, responsible for algorithmic dispatch with sampling-based analysis.
- **Python Bridge**: NumPy `PyArray1` bindings in `src/lib.rs` and the `python/ordr/` package. Data flows as `list → np.ndarray → Rust in-place sort → list`.

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details on how to get started.

## License

`ordr` is licensed under the MIT License. See [LICENSE](LICENSE) for details.
