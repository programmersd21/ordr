# Algorithms API

Complete reference for all sorting algorithms in ordr.

All functions accept `list[int]` or `np.ndarray` and return the same type.
Passing a numpy array sorts it in-place (zero-copy) and returns it.
Passing a list copies it to a numpy array, sorts it, and returns a new list.

## Foundation Algorithms

### bubble()

```python
ordr.bubble(arr: list[int] | np.ndarray) -> list[int] | np.ndarray
```

Bubble sort with early-exit optimization.

**Complexity:**
- Time: O(n²) worst/average, O(n) best
- Space: O(1)
- Stable: Yes

**Best for:** Educational purposes, nearly sorted small arrays

---

### insertion()

```python
ordr.insertion(arr: list[int] | np.ndarray) -> list[int] | np.ndarray
```

Insertion sort.

**Complexity:**
- Time: O(n²) worst/average, O(n) best
- Space: O(1)
- Stable: Yes

**Best for:** Small arrays (< 16 elements), nearly sorted data

---

### merge()

```python
ordr.merge(arr: list[int] | np.ndarray) -> list[int] | np.ndarray
```

Stable merge sort with insertion sort cutoff.

**Complexity:**
- Time: O(n log n)
- Space: O(n)
- Stable: Yes

**Best for:** When stability is required

---

### quick()

```python
ordr.quick(arr: list[int] | np.ndarray) -> list[int] | np.ndarray
```

Quicksort with median-of-three pivot selection.

**Complexity:**
- Time: O(n log n) average, O(n²) worst
- Space: O(log n)
- Stable: No

**Best for:** General-purpose sorting

---

### heap()

```python
ordr.heap(arr: list[int] | np.ndarray) -> list[int] | np.ndarray
```

Heapsort implementation.

**Complexity:**
- Time: O(n log n) guaranteed
- Space: O(1)
- Stable: No

**Best for:** When guaranteed O(n log n) and O(1) space is needed

---

## Production Algorithms

### intro()

```python
ordr.intro(arr: list[int] | np.ndarray) -> list[int] | np.ndarray
```

IntroSort: hybrid quicksort with heapsort fallback.

**Complexity:**
- Time: O(n log n) guaranteed
- Space: O(log n)
- Stable: No

**Best for:** General-purpose unstable sorting

**Details:**
- Starts with quicksort
- Switches to heapsort when recursion depth exceeds 2 * log₂(n)
- Uses insertion sort for small partitions (< 16 elements)

---

### tim()

```python
ordr.tim(arr: list[int] | np.ndarray) -> list[int] | np.ndarray
```

TimSort-inspired stable sort.

**Complexity:**
- Time: O(n log n) worst, O(n) best
- Space: O(n)
- Stable: Yes

**Best for:** Nearly sorted data, real-world data with natural runs

**Details:**
- Divides array into runs of minimum size
- Extends short runs with insertion sort
- Merges runs iteratively
- Optimized for partially sorted data

---

### pdq()

```python
ordr.pdq(arr: list[int] | np.ndarray) -> list[int] | np.ndarray
```

Pattern-Defeating QuickSort.

**Complexity:**
- Time: O(n log n) average and worst
- Space: O(log n)
- Stable: No

**Best for:** Random data, general-purpose high-performance sorting

**Details:**
- Median-of-three pivoting for small arrays
- Tukey's ninther for large arrays (> 128 elements)
- Branchless Hoare partition with prefetching
- Sorting networks for n=2-4 optimized sub-arrays
- Pattern-breaking optimizations (detects sorted/reverse)
- Heapsort fallback for bad partitions

---

### radix()

```python
ordr.radix(arr: list[int] | np.ndarray) -> list[int] | np.ndarray
```

LSD Radix Sort for signed integers.

**Complexity:**
- Time: O(n * k) where k is number of digits
- Space: O(n + radix)
- Stable: Yes

**Best for:** Large integer arrays with reasonable value ranges

**Details:**
- Uses 10 buckets (decimal digit based)
- Handles negative numbers by splitting into negative and positive groups
- Adaptive pass count based on value range
- Most efficient for large arrays of integers

---

## Parallel Algorithms

### par_sort()

```python
ordr.par_sort(arr: list[int] | np.ndarray) -> list[int] | np.ndarray
```

Parallel stable sort using Rayon.

**Complexity:**
- Time: O(n log n)
- Space: O(n)
- Stable: Yes

**Best for:** Large datasets (> 10,000 elements) when stability is needed

---

### par_sort_unstable()

```python
ordr.par_sort_unstable(arr: list[int] | np.ndarray) -> list[int] | np.ndarray
```

Parallel unstable sort using Rayon.

**Complexity:**
- Time: O(n log n)
- Space: O(log n)
- Stable: No

**Best for:** Large datasets (> 10,000 elements) when stability is not required

**Details:**
- Faster than stable parallel sort
- Automatically falls back to sequential sort for small arrays

### par_merge()

```python
ordr.par_merge(arr: list[int] | np.ndarray) -> list[int] | np.ndarray
```

Parallel merge sort using Rayon's `join` for recursive splitting.

**Complexity:**
- Time: O(n log n)
- Space: O(n)
- Stable: Yes

**Best for:** Large datasets when a stable parallel sort is needed

---

## Adaptive Algorithm

### smart()

```python
ordr.smart(arr: list[int] | np.ndarray) -> list[int] | np.ndarray
```

Adaptive algorithm selector that analyzes data and chooses the best algorithm.

**Complexity:** Varies based on selected algorithm

**Best for:** General use when you want optimal performance

**Selection Strategy:**
1. **Small arrays (< 16):** insertion sort
2. **Nearly sorted (> 90%):** timsort
3. **High duplicates (> 50%):** timsort
4. **Very large (> 100k):** parallel sort (par_sort_unstable)
5. **Integer-optimized (>= 1k, range < 1M):** radix sort
6. **Default:** pdqsort

**Example:**

```python
import ordr

# Smart sort automatically adapts
small = [5, 2, 8, 1]  # Uses insertion
nearly_sorted = list(range(100))  # Uses timsort
random_data = [9, 2, 7, 4, 1]  # Uses pdqsort
large = list(range(200000))  # Uses parallel sort
integers = [170, 45, 75, 90, 802, 24, 2, 66]  # May use radix

for arr in [small, nearly_sorted, random_data, large, integers]:
    result = ordr.smart(arr)
```

## Comparison Table

| Algorithm | Time (Avg) | Time (Worst) | Space | Stable | Best Use Case |
|-----------|------------|--------------|-------|--------|---------------|
| bubble | O(n²) | O(n²) | O(1) | Yes | Educational |
| insertion | O(n²) | O(n²) | O(1) | Yes | Small/nearly sorted |
| merge | O(n log n) | O(n log n) | O(n) | Yes | Stability required |
| quick | O(n log n) | O(n²) | O(log n) | No | General purpose |
| heap | O(n log n) | O(n log n) | O(1) | No | Guaranteed performance |
| intro | O(n log n) | O(n log n) | O(log n) | No | General purpose |
| tim | O(n log n) | O(n log n) | O(n) | Yes | Real-world data |
| pdq | O(n log n) | O(n log n) | O(log n) | No | High performance |
| radix | O(nk) | O(nk) | O(n) | Yes | Integer arrays |
| par_sort | O(n log n) | O(n log n) | O(n) | Yes | Large datasets |
| par_sort_unstable | O(n log n) | O(n log n) | O(log n) | No | Large datasets (fastest) |
| par_merge | O(n log n) | O(n log n) | O(n) | Yes | Large stable datasets |
| smart | Adaptive | Adaptive | Varies | Varies | General use |
