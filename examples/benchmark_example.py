"""Benchmarking examples with ordr."""

from ordr.benchmark import compare, display_comparison, profile

# Compare algorithms on random data
print("Comparing algorithms on random data (10,000 elements):")
results = compare(size=10000, pattern="random")
display_comparison(results)

print("\n" + "=" * 60 + "\n")

# Compare on nearly sorted data
print("Comparing algorithms on nearly sorted data:")
results = compare(
    size=10000, pattern="nearly_sorted", algorithms=["smart", "tim", "pdq", "intro", "builtin"]
)
display_comparison(results)

print("\n" + "=" * 60 + "\n")

# Profile smart sort across different sizes
print("Profiling smart sort across different sizes:")
profile(sizes=[1000, 10000, 100000], pattern="random", algorithm="smart")

print("\n" + "=" * 60 + "\n")

# Compare on duplicate-heavy data
print("Comparing on duplicate-heavy data:")
results = compare(size=10000, pattern="duplicates", algorithms=["smart", "tim", "quick", "builtin"])
display_comparison(results)
