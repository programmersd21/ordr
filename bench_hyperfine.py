"""Benchmark helper for hyperfine.

Usage:
    python bench_hyperfine.py generate <size> <pattern> <outfile>
    python bench_hyperfine.py run <algo> <datafile> [--iters N]
"""

import pickle
import random
import sys

import ordr


def generate(size, pattern, outpath):
    random.seed(42)
    if pattern == "random":
        data = [random.randint(-1_000_000, 1_000_000) for _ in range(size)]
    elif pattern == "sorted":
        data = list(range(size))
    elif pattern == "reverse":
        data = list(range(size, 0, -1))
    with open(outpath, "wb") as f:
        pickle.dump(data, f)


def run(algo, datapath, iters):
    with open(datapath, "rb") as f:
        arr = pickle.load(f)
    for _ in range(iters):
        if algo == "builtin":
            sorted(arr)
        else:
            getattr(ordr, algo)(arr)


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "generate":
        generate(int(sys.argv[2]), sys.argv[3], sys.argv[4])
    elif mode == "run":
        iters = int(sys.argv[5]) if len(sys.argv) > 5 and sys.argv[4] == "--iters" else 100
        run(sys.argv[2], sys.argv[3], iters)
    else:
        print(f"Unknown mode: {mode}", file=sys.stderr)
        sys.exit(1)
