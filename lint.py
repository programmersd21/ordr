import subprocess
import sys


def run(cmd: list[str], message: str) -> None:
    print(f"\n{message}...")
    subprocess.run(cmd, check=True)


def run_lint() -> None:
    run(
        ["ruff", "format", "python/", "tests/", "examples/"],
        "Running ruff format",
    )

    run(
        ["ruff", "check", "--fix", "python/", "tests/", "examples/"],
        "Running ruff check",
    )

    run(
        ["mypy", "python/ordr"],
        "Running mypy",
    )

    run(
        ["cargo", "fmt", "--all"],
        "Running cargo fmt",
    )

    run(
        [
            "cargo",
            "clippy",
            "--all-targets",
            "--all-features",
            "--",
            "-D",
            "warnings",
        ],
        "Running cargo clippy",
    )

    run(
        ["pytest", "tests/"],
        "Running pytest",
    )

    print("\nAll checks passed.")


if __name__ == "__main__":
    try:
        run_lint()
    except subprocess.CalledProcessError:
        print("\nChecks failed.")
        sys.exit(1)
        