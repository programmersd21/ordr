# Benchmarking Guide

Benchmarking is a first-class citizen in `ordr`. Without rigorous performance measurement, optimization claims are meaningless.

## The `ordr` Philosophy

We don't just benchmark random data. We benchmark against diverse data patterns that reflect real-world use cases:

1.  **Random**: Standard uniform distribution.
2.  **Sorted**: Already in order (detects O(n) optimizations).
3.  **Reverse**: Decreasing order (detects O(n) optimizations).
4.  **Nearly Sorted**: Mostly in order with few inversions (TimSort's strength).
5.  **Duplicates**: Many equal elements (3-way partitioning's strength).

## Running Benchmarks from CLI

The easiest way to benchmark is using the `ordr bench` command.

```bash
# Benchmark all algorithms on random data
ordr bench --size 10000

# Benchmark specific algorithms on nearly sorted data
ordr bench --size 50000 --pattern nearly_sorted --algorithms smart,tim,builtin
```

### Profiling across sizes

To see how an algorithm scales:

```bash
ordr prof --algorithm smart --sizes 100,1000,10000,100000
```

## Python API Benchmarking

You can use the benchmarking utilities in your own scripts:

```python
from ordr.benchmark import compare, display_comparison

# Run a comparison
results = compare(size=20000, pattern="duplicates")

# Display a beautiful table
display_comparison(results)
```

## Rust-Level Benchmarks (Criterion)

For high-precision Rust-level benchmarks, we use [Criterion](https://github.com/bheisler/criterion.rs).

```bash
cargo bench
```

This generates detailed HTML reports in `target/criterion/report/index.html`.

## Interpreting Results

*   **vs Baseline**: We always compare against Python's built-in `sorted()` (which is a highly optimized C-based TimSort).
*   **Time per element**: Useful for seeing the constant factor in O(n log n).
*   **Stability**: If you need stability, only compare `tim`, `merge`, `radix`, and `par_sort`.

## Best Practices

1.  **Clean Environment**: Close other applications when running benchmarks.
2.  **Warm-up**: Run a few iterations before measuring (handled automatically by `benchmark_function`).
3.  **Multiple Sizes**: Some algorithms only show their strength at scale (e.g., `par_sort`).
4.  **Statistically Significant**: We use the **median** of multiple runs to minimize the impact of system noise.
