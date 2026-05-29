import ordr


def test_smart_small_array():
    arr = [3, 1, 4, 1, 5]
    result = ordr.smart(arr)
    assert result == [1, 1, 3, 4, 5]


def test_smart_nearly_sorted():
    arr = list(range(100))
    arr[10], arr[11] = arr[11], arr[10]
    arr[50], arr[51] = arr[51], arr[50]

    result = ordr.smart(arr)
    assert result == sorted(arr)


def test_smart_duplicates():
    arr = [5] * 50 + [1] * 50 + [3] * 50
    result = ordr.smart(arr)
    assert result == sorted(arr)


def test_smart_random():
    arr = [9, 2, 7, 4, 1, 8, 3, 6, 5, 10]
    result = ordr.smart(arr)
    assert result == sorted(arr)


def test_smart_large_array():
    arr = list(range(50000, 0, -1))
    result = ordr.smart(arr)
    assert result == sorted(arr)


def test_smart_empty():
    assert ordr.smart([]) == []


def test_smart_single():
    assert ordr.smart([42]) == [42]


def test_smart_negative():
    arr = [-5, -1, -10, 0, 3, -2, 7]
    result = ordr.smart(arr)
    assert result == sorted(arr)


def test_smart_correctness():
    test_cases = [
        [3, 1, 4, 1, 5, 9, 2, 6],
        list(range(100)),
        list(range(100, 0, -1)),
        [1] * 100,
        [-50, -25, 0, 25, 50],
    ]

    for arr in test_cases:
        result = ordr.smart(arr.copy())
        assert result == sorted(arr), f"Failed on {arr[:10]}..."
