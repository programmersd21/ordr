import ordr


def test_all_same_elements():
    arr = [5] * 100
    for algo in [ordr.smart, ordr.pdq, ordr.quick, ordr.merge]:
        result = algo(arr.copy())
        assert result == arr


def test_two_elements():
    assert ordr.smart([2, 1]) == [1, 2]
    assert ordr.smart([1, 2]) == [1, 2]


def test_alternating_pattern():
    arr = [1, 100, 2, 99, 3, 98, 4, 97]
    result = ordr.smart(arr)
    assert result == sorted(arr)


def test_extreme_values():
    arr = [-(2**60), 2**60, 0, -(2**59), 2**59]
    result = ordr.smart(arr)
    assert result == sorted(arr)


def test_many_duplicates_few_unique():
    arr = [1, 2, 3] * 100
    result = ordr.smart(arr)
    assert result == sorted(arr)


def test_already_sorted_large():
    arr = list(range(10000))
    result = ordr.smart(arr)
    assert result == arr


def test_reverse_sorted_large():
    arr = list(range(10000, 0, -1))
    result = ordr.smart(arr)
    assert result == list(range(1, 10001))


def test_mountain_pattern():
    arr = list(range(50)) + list(range(50, 0, -1))
    result = ordr.smart(arr)
    assert result == sorted(arr)


def test_valley_pattern():
    arr = list(range(50, 0, -1)) + list(range(50))
    result = ordr.smart(arr)
    assert result == sorted(arr)


def test_radix_with_zeros():
    arr = [0] * 50 + [1, 2, 3, -1, -2, -3]
    result = ordr.radix(arr)
    assert result == sorted(arr)


def test_parallel_threshold():
    arr = list(range(20000, 0, -1))
    result = ordr.par_sort_unstable(arr)
    assert result == list(range(1, 20001))
