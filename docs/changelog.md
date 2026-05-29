# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-05-29

### Changed

- **Zero-Copy FFI**: All native `#[pyfunction]` signatures changed from `Vec<i64> -> Vec<i64>` to `(Python<'_>, &PyArray1<i64>) -> PyResult<()>`. Sorting happens in-place on the numpy array buffer. Python wrapper converts list → numpy → native in-place → list.
- **mimalloc Global Allocator**: Replaced system allocator with mimalloc for ~2x faster allocation-heavy operations.
- **LTO="fat"**: Changed from `lto = true` to `lto = "fat"` for improved cross-crate optimization.
- **PDQSort Partition**: Switched from block partitioning to branchless Hoare partition with `_mm_prefetch` hints.
- **Sorting Networks**: Added verified optimal sorting networks for n=2,3,4 used by PDQSort's small-array path.
- **Internal Functions Public**: `smart_sort`, `introsort`, `quicksort` made public Rust functions for direct `&mut [i64]` usage.

### Added

- NumPy array support: functions accept `np.ndarray` directly (zero-copy in-place).
- Sorting networks module (`src/algorithms/sorting_network.rs`).
- `Makefile` with `bench-compare`, `bench-all`, `bench-rust`, `clean` targets.

### Fixed

- PDQSort duplicate-handling correctness bug.
- Rust benchmarks not compiling after PyArray1 migration.
- CI workflow now triggers only on `Cargo.toml`/`pyproject.toml` changes or manual dispatch.

### Performance

| Algorithm | Before (1M random) | After (1M random) | Speedup |
|-----------|-------------------|-------------------|---------|
| smart | 475 ms | 63 ms | **7.5x** |
| pdq | 547 ms | 160 ms | **3.4x** |
| builtin | 671 ms | 267 ms | **2.5x** |

## [0.1.1] - 2026-05-29

### Changed

- **Enhanced Smart Dispatch**: `ordr.smart()` now includes radix sort suitability detection and parallel sort dispatch for large arrays (>100k).
- **Improved TimSort Implementation**: Fixed merge-phase index bug causing panics on large arrays. Rewrote with iterative merge passes for correctness.

### Added

- `par_sort_unstable()` exposed as a public API function.
- `par_merge()` exposed as a public API function.
- Internal `par_sort_unstable_impl()` for use by the adaptive dispatcher.
- Radix suitability heuristics in the adaptive dispatch engine.

### Fixed

- All 14 Rust compilation errors from stub algorithm files.
- PyO3 0.20 compatibility.
- Benchmark imports (crate-type needed `rlib`).
- 119 failing tests → all 128 passing.

## [0.2.0] - 2026-05-29

### Added

- **Core Algorithms**: PDQSort, TimSort, IntroSort, Radix Sort in Rust.
- **Foundation Algorithms**: Bubble Sort, Insertion Sort, Merge Sort, Heap Sort, Quick Sort.
- **Adaptive Dispatch**: `ordr.smart()` engine for intelligent algorithm selection.
- **Parallel Sorting**: Rayon-based parallel sorting.
- **Python Bindings**: PyO3 and Maturin FFI.
- **CLI Tool**: `ordr` command with benchmarking, profiling, and visualization.
- **Visualization**: Rich-powered terminal visualization.
- **Benchmarking**: Benchmarking suite comparing against Python's `sorted()`.
- **Documentation**: MkDocs documentation.
- **CI/CD**: GitHub Actions.

### Fixed

- Initial release.
