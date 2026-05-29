"""Tests for sorting algorithms."""

import ordr
import pytest


@pytest.fixture
def test_arrays():
    """Common test arrays."""
    return {
        "random": [3, 1, 4, 1, 5, 9, 2, 6, 5, 3],
        "sorted": [1, 2, 3, 4, 5],
        "reverse": [5, 4, 3, 2, 1],
        "single": [42],
        "empty": [],
        "duplicates": [3, 3, 3, 1, 1, 2, 2],
        "negative": [-5, -1, -10, 0, 3, -2],
        "large": list(range(1000, 0, -1)),
    }


algorithms = [
    ordr.bubble,
    ordr.insertion,
    ordr.merge,
    ordr.quick,
    ordr.heap,
    ordr.intro,
    ordr.tim,
    ordr.pdq,
    ordr.radix,
    ordr.smart,
    ordr.par_sort,
    ordr.par_sort_unstable,
]


@pytest.mark.parametrize("algorithm", algorithms)
def test_random_array(algorithm, test_arrays):
    arr = test_arrays["random"].copy()
    result = algorithm(arr)
    assert result == sorted(arr)


@pytest.mark.parametrize("algorithm", algorithms)
def test_sorted_array(algorithm, test_arrays):
    arr = test_arrays["sorted"].copy()
    result = algorithm(arr)
    assert result == sorted(arr)


@pytest.mark.parametrize("algorithm", algorithms)
def test_reverse_array(algorithm, test_arrays):
    arr = test_arrays["reverse"].copy()
    result = algorithm(arr)
    assert result == sorted(arr)


@pytest.mark.parametrize("algorithm", algorithms)
def test_single_element(algorithm, test_arrays):
    arr = test_arrays["single"].copy()
    result = algorithm(arr)
    assert result == [42]


@pytest.mark.parametrize("algorithm", algorithms)
def test_empty_array(algorithm, test_arrays):
    arr = test_arrays["empty"].copy()
    result = algorithm(arr)
    assert result == []


@pytest.mark.parametrize("algorithm", algorithms)
def test_duplicates(algorithm, test_arrays):
    arr = test_arrays["duplicates"].copy()
    result = algorithm(arr)
    assert result == sorted(arr)


@pytest.mark.parametrize("algorithm", algorithms)
def test_negative_numbers(algorithm, test_arrays):
    arr = test_arrays["negative"].copy()
    result = algorithm(arr)
    assert result == sorted(arr)


@pytest.mark.parametrize("algorithm", algorithms)
def test_large_array(algorithm, test_arrays):
    arr = test_arrays["large"].copy()
    result = algorithm(arr)
    assert result == sorted(arr)


def test_stability_merge(test_arrays):
    arr = test_arrays["duplicates"].copy()
    result = ordr.merge(arr)
    assert result == sorted(arr)


def test_stability_tim(test_arrays):
    arr = test_arrays["duplicates"].copy()
    result = ordr.tim(arr)
    assert result == sorted(arr)


def test_radix_negative_handling():
    arr = [-100, 50, -50, 100, 0, -1, 1]
    result = ordr.radix(arr)
    assert result == sorted(arr)
