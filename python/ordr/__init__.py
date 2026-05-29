"""ordr: High-performance adaptive sorting for Python, powered by Rust."""

from typing import Any

import numpy as np

import ordr._ordr as _native


def _prepare(arr: Any) -> tuple[np.ndarray, bool]:
    was_ndarray = isinstance(arr, np.ndarray)
    native = arr if was_ndarray and arr.dtype == np.int64 else np.asarray(arr, dtype=np.int64)
    return native, was_ndarray


def bubble(arr: Any) -> Any:
    native, was = _prepare(arr)
    _native.bubble(native)
    return native if was else native.tolist()


def heap(arr: Any) -> Any:
    native, was = _prepare(arr)
    _native.heap(native)
    return native if was else native.tolist()


def insertion(arr: Any) -> Any:
    native, was = _prepare(arr)
    _native.insertion(native)
    return native if was else native.tolist()


def intro(arr: Any) -> Any:
    native, was = _prepare(arr)
    _native.intro(native)
    return native if was else native.tolist()


def merge(arr: Any) -> Any:
    native, was = _prepare(arr)
    _native.merge(native)
    return native if was else native.tolist()


def par_merge(arr: Any) -> Any:
    native, was = _prepare(arr)
    _native.par_merge(native)
    return native if was else native.tolist()


def par_sort(arr: Any) -> Any:
    native, was = _prepare(arr)
    _native.par_sort(native)
    return native if was else native.tolist()


def par_sort_unstable(arr: Any) -> Any:
    native, was = _prepare(arr)
    _native.par_sort_unstable(native)
    return native if was else native.tolist()


def pdq(arr: Any) -> Any:
    native, was = _prepare(arr)
    _native.pdq(native)
    return native if was else native.tolist()


def quick(arr: Any) -> Any:
    native, was = _prepare(arr)
    _native.quick(native)
    return native if was else native.tolist()


def radix(arr: Any) -> Any:
    native, was = _prepare(arr)
    _native.radix(native)
    return native if was else native.tolist()


def smart(arr: Any) -> Any:
    native, was = _prepare(arr)
    _native.smart(native)
    return native if was else native.tolist()


def tim(arr: Any) -> Any:
    native, was = _prepare(arr)
    _native.tim(native)
    return native if was else native.tolist()


__version__ = "0.1.0"

__all__ = [
    "bubble",
    "heap",
    "insertion",
    "intro",
    "merge",
    "par_merge",
    "par_sort",
    "par_sort_unstable",
    "pdq",
    "quick",
    "radix",
    "smart",
    "tim",
]
