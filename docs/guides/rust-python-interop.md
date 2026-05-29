# Rust-Python Interop

`ordr` uses **PyO3**, **Maturin**, and the **numpy** crate to bridge the performance of Rust with the ergonomics of Python.

## Architecture

The interop layer has three components:

1.  **Rust Backend**: High-performance sorting implementations in `src/`, operating on `&mut [i64]` slices.
2.  **PyO3 + numpy Bindings**: Glue code in `src/lib.rs` and each algorithm module that exposes Rust functions taking `&PyArray1<i64>`.
3.  **Python Wrapper**: The package in `python/ordr/` that provides a clean, typed API with list → numpy → list conversion.

## Data Flow

When you call `ordr.smart(arr)` in Python:

1.  **Python `_prepare()`**: Converts `list` to `np.ndarray` via `np.asarray(arr, dtype=np.int64)`. If `arr` is already an int64 numpy array, passes through without copying.
2.  **Rust `#[pyfunction]`**: Receives `&PyArray1<i64>`, obtains a mutable slice via `unsafe { arr.as_array_mut() }`.
3.  **In-place sort**: Rust sorts the data directly in the numpy array buffer.
4.  **Return**: Python wrapper returns the sorted result (same ndarray if input was ndarray, or `tolist()` if input was list).

### Why `PyArray1<i64>`?

- Zero-copy access to numpy's internal memory buffer.
- Eliminates the `Vec<i64>` copy that was required with the previous FFI approach.
- Accepts both Python lists (after conversion in the wrapper) and numpy arrays.
- `i64` provides a 1:1 mapping for integers up to 2^63-1.

## The Build System (Maturin)

**Maturin** handles:
- Compiling the Rust code into a shared library.
- Generating the Python wheel.
- Managing PyO3 linkage.

### Local Development

```bash
# Develop mode
maturin develop --release
```

## Performance Considerations

### FFI Overhead

Crossing the Python ↔ Rust boundary has a small cost.
- For lists: the `np.asarray` conversion is O(n) and involves a copy.
- For numpy arrays: zero-copy at the FFI boundary.

### Release vs Debug

**NEVER benchmark with a debug build.**
Rust's performance relies on LLVM optimizations active only in `--release` mode.

```bash
maturin develop --release   # for benchmarking/production
maturin develop             # NOT for performance
```

## Error Handling

We use `PyResult` in Rust to safely propagate errors to Python as exceptions.

```rust
#[pyfunction]
pub fn sort<'py>(_py: Python<'py>, arr: &PyArray1<i64>) -> PyResult<()> {
    let mut slice = unsafe { arr.as_array_mut() };
    let a = slice.as_slice_mut().unwrap();
    a.sort();
    Ok(())
}
```

## Type Safety and IDE Support

`ordr` is fully typed and PEP 561 compliant:

1.  **Type Stubs (`.pyi`)**: We provide type stubs for the native Rust extension in `python/ordr/_ordr.pyi`.
2.  **Inline Type Hints**: All Python modules use standard Python type hints.
3.  **`py.typed`**: The package includes a `py.typed` marker file for Mypy/Pyright support.
