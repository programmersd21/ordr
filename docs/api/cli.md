# CLI Reference

Command-line interface for ordr.

## Commands

### info

Display information about ordr.

```bash
ordr info
```

Shows available algorithms, features, and usage examples.

---

### bench

Run sorting benchmarks.

```bash
ordr bench [OPTIONS]
```

**Options:**
- `--size INTEGER`: Array size (default: 10000)
- `--pattern TEXT`: Data pattern (default: "random")
  - `random`: Random data
  - `sorted`: Already sorted
  - `reverse`: Reverse sorted
  - `nearly_sorted`: 90% sorted
  - `duplicates`: Many duplicates
- `--algorithms TEXT`: Comma-separated algorithm names (empty = all)

**Examples:**

```bash
# Basic benchmark
ordr bench

# Custom size and pattern
ordr bench --size 50000 --pattern nearly_sorted

# Specific algorithms
ordr bench --algorithms "smart,pdq,tim"

# Duplicate-heavy data
ordr bench --size 20000 --pattern duplicates
```

---

### prof

Profile an algorithm across different sizes.

```bash
ordr prof [OPTIONS]
```

**Options:**
- `--algorithm TEXT`: Algorithm to profile (default: "smart")
- `--pattern TEXT`: Data pattern (default: "random")
- `--sizes TEXT`: Comma-separated sizes (default: "1000,10000,100000")

**Examples:**

```bash
# Profile smart sort
ordr prof --algorithm smart

# Profile pdqsort on nearly sorted data
ordr prof --algorithm pdq --pattern nearly_sorted

# Custom sizes
ordr prof --algorithm tim --sizes "5000,50000,500000"
```

---

### viz

Visualize a sorting algorithm.

```bash
ordr viz [OPTIONS]
```

**Options:**
- `--algorithm TEXT`: Algorithm to visualize (default: "bubble")
  - `bubble`, `insertion`, `quick`, `merge`
- `--size INTEGER`: Array size (default: 20, recommended: 10-30)
- `--delay FLOAT`: Delay between frames in seconds (default: 0.05)

**Examples:**

```bash
# Visualize bubble sort
ordr viz --algorithm bubble --size 20

# Visualize quicksort with slower animation
ordr viz --algorithm quick --size 25 --delay 0.1

# Fast insertion sort visualization
ordr viz --algorithm insertion --size 15 --delay 0.02
```

---

## Complete Examples

### Benchmark Workflow

```bash
# 1. Get info
ordr info

# 2. Quick benchmark
ordr bench

# 3. Test on nearly sorted data
ordr bench --size 20000 --pattern nearly_sorted

# 4. Profile smart sort
ordr prof --algorithm smart --sizes "10000,100000,1000000"
```

### Visualization Workflow

```bash
# Compare different algorithms visually
ordr viz --algorithm bubble --size 20
ordr viz --algorithm insertion --size 20
ordr viz --algorithm quick --size 20
ordr viz --algorithm merge --size 20
```
