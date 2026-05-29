import os
import subprocess
import sys
from pathlib import Path


def run_examples():
    example_dir = Path("examples")

    if not example_dir.exists():
        print(f"[ERROR] Directory not found: {example_dir.resolve()}")
        sys.exit(1)

    examples = sorted(example_dir.glob("*.py"))

    if not examples:
        print("[WARN] No example files found.")
        return

    print("=" * 80)
    print(f"Python Executable : {sys.executable}")
    print(f"Examples Directory: {example_dir.resolve()}")
    print(f"Total Examples    : {len(examples)}")
    print("=" * 80)

    failed = []

    for index, example in enumerate(examples, start=1):
        print()
        print("=" * 80)
        print(f"[{index}/{len(examples)}] Running: {example.name}")
        print("=" * 80)

        command = [sys.executable, str(example)]

        print("Command:")
        print(" ", " ".join(command))
        print("-" * 80)

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
        )

        print(f"Exit Code: {result.returncode}")

        if result.stdout.strip():
            print("\n[STDOUT]")
            print(result.stdout.rstrip())

        if result.stderr.strip():
            print("\n[STDERR]")
            print(result.stderr.rstrip())

        if result.returncode == 0:
            print(f"\n[SUCCESS] {example.name}")
        else:
            print(f"\n[FAILED] {example.name}")
            failed.append(example.name)

    print()
    print("=" * 80)

    if failed:
        print("[SUMMARY] Some examples failed:")
        for name in failed:
            print(f"  - {name}")

        print(f"\nResult: {len(failed)} failed / {len(examples)} total")
        print("=" * 80)

        sys.exit(1)

    print("[SUMMARY] All examples passed successfully.")
    print("=" * 80)


if __name__ == "__main__":
    run_examples()
    