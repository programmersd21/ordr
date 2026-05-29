# Benchmark API

Tools for measuring and comparing sorting performance.

## Functions

### compare()

```python
compare(
    size: int = 10000,
    pattern: str = "random",
    algorithms: list[str] | None = None
) -> dict[str, float]
```

Compare sorting algorithms on specific data pattern.

**Parameters:**
- `size`: Array size
- `pattern`: Data pattern (`"random"`, `"sorted"`, `"reverse"`, `"nearly_sorted"`, `"duplicates"`)
- `algorithms`: List of algorithm names (None = all)

**Returns:** Dictionary mapping algorithm names to median times (ms)

**Example:**

```python
from ordr.benchmark import compare, display_comparison

results = compare(size=10000, pattern="random")
display_comparison(results)
```

---

### profile()

```python
profile(
    sizes: list[int] = [1000, 10000, 100000],
    pattern: str = "random",
    algorithm: str = "smart"
) -> None
```

Profile an algorithm across different input sizes.

**Example:**

```python
from ordr.benchmark import profile

profile(
    sizes=[1000, 10000, 100000],
    pattern="random",
    algorithm="smart"
)
```

---

### display_comparison()

```python
display_comparison(
    results: dict[str, float],
    baseline: str = "builtin"
) -> None
```

Display benchmark results in a rich table.

---

## Data Generators

### generate_random()

```python
generate_random(size: int) -> list[int]
```

Generate random array.

---

### generate_sorted()

```python
generate_sorted(size: int) -> list[int]
```

Generate sorted array.

---

### generate_reverse()

```python
generate_reverse(size: int) -> list[int]
```

Generate reverse sorted array.

---

### generate_nearly_sorted()

```python
generate_nearly_sorted(size: int) -> list[int]
```

Generate nearly sorted array (~90% sorted).

---

### generate_duplicates()

```python
generate_duplicates(size: int) -> list[int]
```

Generate array with many duplicates.

---

## Example Usage

```python
from ordr.benchmark import compare, profile, display_comparison

# Compare on random data
results = compare(size=10000, pattern="random")
display_comparison(results)

# Compare specific algorithms
results = compare(
    size=10000,
    pattern="nearly_sorted",
    algorithms=["smart", "tim", "pdq"]
)
display_comparison(results)

# Profile across sizes
profile(
    sizes=[1000, 10000, 100000],
    pattern="random",
    algorithm="smart"
)
```
