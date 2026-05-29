# Internal Architecture

`ordr` is designed as a modular, professional systems library.

## Project Structure

```text
ordr/
├── src/                # Rust Source
│   ├── algorithms/     # Individual sorting implementations
│   ├── adaptive/       # Logic for smart dispatch
│   ├── parallel/       # Rayon-based parallel sorting
│   └── utils/          # Data analysis and metrics
├── python/ordr/        # Python Source
│   ├── benchmark.py    # Benchmarking suite
│   ├── visualize.py    # Terminal visualization
│   └── cli.py          # Typer-based CLI
└── tests/              # Cross-language test suite
```

## Design Principles

1.  **Performance First**: All performance-critical code is in Rust. Branchless partition, prefetching, and LTO.
2.  **Zero-Cost Abstractions**: The Python layer is a thin wrapper. Native operations happen in-place on numpy array buffers.
3.  **No Placeholders**: Every algorithm is fully implemented with professional optimizations.

## The Rust Core

Each algorithm in `src/algorithms/` follows a consistent pattern:
- A `#[pyfunction]` that takes `&PyArray1<i64>` and sorts in-place, returning `PyResult<()>`.
- Internal sorting functions that operate on `&mut [i64]` slices (many are `pub` for direct use by other Rust crates).
- Verified sorting networks for n=2,3,4 used by PDQSort's small-array path.

### Algorithm Selection

- **Foundational**: Textbook algorithms (Bubble, Insertion, Merge, Quick).
- **Production**: State-of-the-art algorithms (TimSort, PDQSort, IntroSort).
- **Specialized**: Non-comparison or parallel sorts (Radix, ParSort).

## Python Data Flow

When you call `ordr.smart(arr)` in Python:

1.  **`_prepare()`**: If `arr` is a `list`, converts to `np.ndarray` via `np.asarray(arr, dtype=np.int64)`. If `arr` is already a numpy array of dtype `int64`, passes through (zero-copy).
2.  **Native call**: The numpy array pointer is passed as `&PyArray1<i64>` to the Rust `#[pyfunction]`, which obtains a mutable slice via `arr.as_array_mut()`.
3.  **In-place sort**: Rust sorts the data in-place on the numpy array buffer.
4.  **Return**: If input was `list`, returns `native.tolist()`. If input was `np.ndarray`, returns the same array (now sorted).

## FFI Integration

Uses **PyO3** with **numpy** crate. The `PyArray1<i64>` type provides direct access to numpy's internal buffer, avoiding copies at the FFI boundary.

Memory allocation uses an optimized global allocator.

## Parallelism Strategy

- **Rayon** for data-parallelism.
- Parallelism activates for arrays > 10,000 elements.
- Uses `rayon::join` to split workload across cores.

## Testing Strategy

1.  **Python Integration Tests**: Testing the full FFI boundary via pytest.
2.  **Property-Based Testing**: Validating algorithms against random, edge-case, and large datasets.
