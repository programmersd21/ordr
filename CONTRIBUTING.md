# Contributing to ordr

Thank you for your interest in contributing to ordr!

## Development Setup

1. Clone the repository
2. Install dependencies: `uv pip install -e ".[dev]"`
3. Build: `maturin develop --release`
4. Test: `cargo test && pytest`

## Code Style

**Rust:** Run `cargo fmt` and `cargo clippy -- -D warnings`
**Python:** Run `ruff format` and `ruff check`

## Pull Request Process

1. Create a feature branch
2. Add tests for new functionality
3. Update documentation
4. Ensure all tests and lints pass
5. Submit PR with clear description

Use conventional commit format: `feat:`, `fix:`, `docs:`, `perf:`, `test:`

## Algorithm Contributions

- Professional implementations with optimizations
- Comprehensive tests including edge cases
- Add Criterion benchmarks
- Document complexity and use cases

Questions? Open an issue!
