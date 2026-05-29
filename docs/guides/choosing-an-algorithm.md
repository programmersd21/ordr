# Choosing an Algorithm

Guide to selecting the right sorting algorithm for your use case.

## Quick Decision Tree

```
Do you know your data characteristics?
├─ No -> Use smart()
└─ Yes
   ├─ Need stability?
   │  ├─ Yes
   │  │  ├─ Nearly sorted? -> tim()
   │  │  ├─ Large (>100k)? -> par_sort()
   │  │  └─ General -> merge()
   │  └─ No
   │     ├─ Small (<16)? -> insertion()
   │     ├─ Large (>100k)? -> par_sort_unstable()
   │     ├─ Integers only? -> radix()
   │     └─ General -> pdq() or intro()
```

## By Use Case

### General Purpose

**Recommendation: `smart()`**

```python
result = ordr.smart(arr)
```

Automatically adapts to your data. Best default choice.

---

### Maximum Performance (Unstable OK)

**Recommendation: `pdq()`**

```python
result = ordr.pdq(arr)
```

Fastest general-purpose unstable sort. Pattern-defeating optimizations.

---

### Stability Required

**Recommendation: `tim()`**

```python
result = ordr.tim(arr)
```

Stable sort optimized for real-world data with natural runs.

---

### Large Datasets

**Recommendation: `par_sort_unstable()` or `par_sort()`**

```python
# Unstable (fastest)
result = ordr.par_sort_unstable(large_arr)

# Stable
result = ordr.par_sort(large_arr)
```

Leverages multiple cores for arrays > 10,000 elements.

---

### Integer Arrays

**Recommendation: `radix()`**

```python
result = ordr.radix(int_arr)
```

Linear time for integers when range is reasonable.

---

### Nearly Sorted Data

**Recommendation: `tim()`**

```python
result = ordr.tim(nearly_sorted)
```

Approaches O(n) for nearly sorted data.

---

### Small Arrays

**Recommendation: `insertion()`**

```python
result = ordr.insertion(small_arr)
```

Minimal overhead for arrays < 16 elements.

---

## By Data Pattern

| Pattern | Best Algorithm | Why |
|---------|---------------|-----|
| Random | `pdq()` | Pattern-defeating, fast partitioning |
| Sorted | `tim()` | Detects runs, O(n) |
| Reverse | `tim()` or `pdq()` | Tim detects reverse runs |
| Nearly sorted | `tim()` | Optimized for natural runs |
| Many duplicates | `tim()` or `radix()` | Stable handling or linear time |
| Large random | `par_sort_unstable()` | Parallel speedup |
| Integers | `radix()` | Linear time |

## By Requirements

### Need Guaranteed O(n log n)?

Use `intro()` or `heap()`:

```python
result = ordr.intro(arr)  # Preferred
result = ordr.heap(arr)   # If O(1) space needed
```

### Need Stability?

Use `tim()`, `merge()`, or `par_sort()`:

```python
result = ordr.tim(arr)      # Best for most cases
result = ordr.merge(arr)    # Classic stable sort
result = ordr.par_sort(arr) # Large stable datasets
```

### Need O(1) Space?

Use `heap()` or `insertion()`:

```python
result = ordr.heap(arr)      # O(n log n)
result = ordr.insertion(arr) # O(n²) but good for small
```

### Need Parallelism?

Use `par_sort()` or `par_sort_unstable()`:

```python
result = ordr.par_sort_unstable(arr)  # Faster
result = ordr.par_sort(arr)           # Stable
```

## Performance Comparison

Performance on **1,000,000 random integers** (measured with hyperfine, including Python startup):

| Algorithm | Time (ms) | vs builtin |
|-----------|-----------|------------|
| par_sort_unstable | 462 | 1.46x faster |
| smart | 466 | 1.44x faster |
| radix | 502 | 1.34x faster |
| pdq | 517 | 1.30x faster |
| builtin | 673 | baseline |

*Benchmarks measured on Windows with hyperfine 1.20, 3 runs each*

## Common Mistakes

### Incorrect: Always using the same algorithm

```python
# Don't do this for all cases
result = ordr.pdq(arr)
```

Different data patterns benefit from different algorithms.

### Correct: Use smart() or choose based on data

```python
# Better
result = ordr.smart(arr)

# Or choose explicitly
if is_nearly_sorted(arr):
    result = ordr.tim(arr)
else:
    result = ordr.pdq(arr)
```

---

### Incorrect: Using slow algorithms for large data

```python
# Don't do this for large arrays
result = ordr.bubble(large_arr)  # O(n²)!
```

### Correct: Use efficient algorithms

```python
# Better
result = ordr.par_sort_unstable(large_arr)
```

---

### Incorrect: Ignoring stability requirements

```python
# If you need stability, don't use unstable sorts
result = ordr.pdq(arr)  # Unstable!
```

### Correct: Use stable sorts when needed

```python
# Better
result = ordr.tim(arr)  # Stable
```

## Summary

**Default choice:** `smart()` - adapts automatically

**High performance:** `pdq()` - fastest general-purpose

**Stability:** `tim()` - stable and fast

**Large data:** `par_sort_unstable()` - parallel speedup

**Integers:** `radix()` - linear time

**Guaranteed:** `intro()` - O(n log n) guaranteed
