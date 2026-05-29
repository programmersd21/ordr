# Adaptive Dispatch Engine

The "Smart" in `ordr.smart()` comes from our adaptive dispatch engine. Instead of a one-size-fits-all approach, `ordr` analyzes your data and selects the most efficient algorithm dynamically.

## Why Adaptive Sorting?

Different sorting algorithms excel at different data patterns:
- **Quicksort** is fast for random data but can struggle with duplicates or sorted data.
- **TimSort** is incredible for nearly sorted data but has more overhead for random data.
- **Radix Sort** is extremely fast for integers but requires more memory and specific ranges.
- **Parallel Sorts** are great for millions of elements but slow for thousands due to thread overhead.

## The Dispatch Process

When `smart(arr)` is called, the following steps occur:

### 1. Size Check
- **Tiny arrays (< 16)**: Immediately dispatched to **Insertion Sort**. The overhead of more complex algorithms isn't worth it.

### 2. Fast Data Analysis
We use low-overhead sampling to estimate two critical metrics:
- **Presortedness**: The ratio of elements already in order (sampled from up to 100 elements).
- **Duplicate Ratio**: The percentage of elements that are repeated (sampled from up to 100 elements).

### 3. Dispatch Logic

The engine follows a prioritized decision tree:

1. **Nearly Sorted (> 90%)**: Dispatched to **TimSort**. TimSort detects "natural runs" and can sort nearly-sorted data in O(n) time.
2. **High Duplicate Ratio (> 50%)**: Dispatched to **TimSort**. TimSort's stability and merge logic handle duplicates more gracefully than naive quicksorts.
3. **Huge Arrays (> 100,000)**: Dispatched to **Parallel Sort** (`par_sort_unstable`). At this scale, the benefits of multi-core execution significantly outweigh the thread management overhead.
4. **Integer Range Check**: If size >= 1000 and the value range is < 1,000,000 (sampled), **Radix Sort** is selected for linear-time sorting.
5. **Default Case**: Dispatched to **PDQSort (Pattern-Defeating Quicksort)**. This is our fastest unstable sort for general-purpose random data.

## Thresholds

The thresholds used in `src/adaptive/smart.rs` are tuned based on empirical benchmarking:

| Metric | Threshold | Target Algorithm |
| :--- | :--- | :--- |
| Size (Small) | < 16 | Insertion |
| Presortedness | > 0.90 | TimSort |
| Duplicate Ratio | > 0.50 | TimSort |
| Size (Parallel) | > 100,000 | Parallel Sort |
| Size (Radix) | >= 1,000 | Radix Sort |
| Value Range (Radix) | < 1,000,000 | Radix Sort |

## Performance Impact

The analysis phase is designed to be **O(1)** (constant time) relative to the array size by using sampling. This ensures that the time spent deciding which algorithm to use is negligible compared to the sorting time itself.

## Transparency

You can inspect why `smart()` made a specific choice by using the `ordr.benchmark` tools to profile different algorithms against your specific data pattern.
