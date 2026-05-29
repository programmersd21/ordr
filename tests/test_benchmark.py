"""Tests for benchmarking utilities."""

import ordr
import pytest
from ordr.benchmark import (
    benchmark_function,
    compare,
    generate_duplicates,
    generate_nearly_sorted,
    generate_random,
    generate_reverse,
    generate_sorted,
)


def test_generate_random():
    arr = generate_random(100)
    assert len(arr) == 100
    assert all(isinstance(x, int) for x in arr)


def test_generate_sorted():
    arr = generate_sorted(100)
    assert len(arr) == 100
    assert arr == list(range(100))


def test_generate_reverse():
    arr = generate_reverse(100)
    assert len(arr) == 100
    assert arr == list(range(100, 0, -1))


def test_generate_nearly_sorted():
    arr = generate_nearly_sorted(100)
    assert len(arr) == 100
    inversions = sum(1 for i in range(len(arr) - 1) if arr[i] > arr[i + 1])
    assert inversions > 0
    assert inversions < 50


def test_generate_duplicates():
    arr = generate_duplicates(100)
    assert len(arr) == 100
    unique_count = len(set(arr))
    assert unique_count < 50


def test_benchmark_function():
    arr = [3, 1, 4, 1, 5, 9, 2, 6]
    time_ms = benchmark_function(ordr.smart, arr, runs=3)
    assert time_ms > 0
    assert isinstance(time_ms, float)


def test_compare_basic():
    results = compare(size=1000, pattern="random", algorithms=["smart", "pdq"])
    assert "smart" in results
    assert "pdq" in results
    assert all(v > 0 for v in results.values())


def test_compare_patterns():
    patterns = ["random", "sorted", "reverse", "nearly_sorted", "duplicates"]
    for pattern in patterns:
        results = compare(size=500, pattern=pattern, algorithms=["smart"])
        assert "smart" in results
        assert results["smart"] > 0


def test_compare_invalid_pattern():
    with pytest.raises(ValueError):
        compare(size=100, pattern="invalid_pattern")
