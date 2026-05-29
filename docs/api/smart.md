# Smart Sort API

The `smart()` function is ordr's adaptive algorithm selector.

## Overview

```python
ordr.smart(arr: list[int] | np.ndarray) -> list[int] | np.ndarray
```

Analyzes input data characteristics and automatically selects the optimal sorting algorithm.

## How It Works

### Analysis Phase

Smart sort performs lightweight analysis:

1. **Size check** - Determines array size
2. **Presortedness measurement** - Samples up to 100 elements to estimate sortedness
3. **Duplicate ratio** - Estimates proportion of duplicate elements using sampling
4. **Value range check** - Checks if integer range fits radix sort constraints

### Dispatch Logic

```
if size <= 16:
    -> insertion sort
elif presortedness > 90%:
    -> timsort
elif duplicate_ratio > 50%:
    -> timsort
elif size > 100,000:
    -> parallel sort (par_sort_unstable)
elif size >= 1,000 and value_range < 1,000,000:
    -> radix sort
else:
    -> pdqsort (default)
```

## Performance Characteristics

### Analysis Overhead

- **Time:** O(1) for small arrays, O(√n) for large arrays (sampling)
- **Space:** O(1)
- **Overhead:** < 1% for arrays > 1000 elements

### Overall Complexity

Depends on selected algorithm, but guaranteed O(n log n) or better.

## Examples

### Small Array

```python
import ordr

arr = [5, 2, 8, 1, 9]
result = ordr.smart(arr)
# Uses: insertion sort
# Why: size <= 16
```

### Nearly Sorted

```python
arr = list(range(1000))
arr[500], arr[501] = arr[501], arr[500]
result = ordr.smart(arr)
# Uses: timsort
# Why: presortedness > 90%
```

### Random Data

```python
import random
arr = [random.randint(0, 10000) for _ in range(10000)]
result = ordr.smart(arr)
# Uses: pdqsort
# Why: default for random data
```

### Many Duplicates

```python
arr = [1, 2, 3] * 1000
result = ordr.smart(arr)
# Uses: timsort
# Why: duplicate_ratio > 50%
```

### Large Array

```python
arr = list(range(200000, 0, -1))
result = ordr.smart(arr)
# Uses: parallel sort
# Why: size > 100,000
```

### Integer Array (Radix-suitable)

```python
arr = [random.randint(0, 500000) for _ in range(5000)]
result = ordr.smart(arr)
# Uses: radix sort
# Why: size >= 1000 and value range < 1,000,000
```

## When to Use

**Use `smart()` when:**
- You want optimal performance without manual tuning
- Input characteristics vary
- You're unsure which algorithm to choose

**Use specific algorithms when:**
- You know exact data characteristics
- You need guaranteed stability
- You're benchmarking specific algorithms
- You want explicit control

## Tuning

The thresholds are tuned for general use but can be adjusted by using specific algorithms:

```python
# Force timsort for stability
ordr.tim(arr)

# Force pdqsort for speed
ordr.pdq(arr)

# Force parallel for large data
ordr.par_sort_unstable(arr)

# Force radix for integers
ordr.radix(arr)
```

## Comparison with Other Approaches

### vs Python's sorted()

```python
# Python's sorted() - always uses Timsort
sorted(arr)

# ordr.smart() - adapts to data
ordr.smart(arr)
```

For random data, `smart()` is typically faster due to PDQSort.
For nearly sorted data, both perform similarly (both use Timsort-like algorithms).

### vs Always Using PDQSort

```python
# Always PDQ
ordr.pdq(arr)

# Smart dispatch
ordr.smart(arr)
```

Smart dispatch adds minimal overhead but can be significantly faster for:
- Small arrays (insertion sort is faster)
- Nearly sorted arrays (timsort is faster)
- Very large arrays (parallel sort is faster)
- Integer arrays within range (radix sort is faster)

## Implementation Details

### Presortedness Measurement

```rust
pub fn measure_presortedness(arr: &[i64]) -> f64 {
    // Samples up to 100 elements
    // Counts inversions in sample
    // Returns ratio: 1.0 = sorted, 0.0 = reverse sorted
}
```

### Duplicate Ratio Measurement

```rust
pub fn measure_duplicate_ratio(arr: &[i64]) -> f64 {
    // Samples up to 100 elements
    // Uses HashSet to detect duplicates
    // Returns ratio: 0.0 = all unique, 1.0 = all same
}
```

### Radix Suitability

```rust
fn is_radix_suitable(arr: &[i64]) -> bool {
    // Requires size >= 1000
    // Samples to find min/max
    // Checks if range < 1,000,000
}
```

## Benchmarks

Performance on **100,000 random integers** (in-process timing):

| Algorithm | Time (ms) | vs builtin |
|-----------|-----------|------------|
| par_sort | 7.1 | 2.6x faster |
| par_sort_unstable | 8.1 | 2.2x faster |
| radix | 8.7 | 2.1x faster |
| smart | 13.1 | 1.4x faster |
| pdq | 13.4 | 1.4x faster |
| builtin | 18.2 | baseline |
