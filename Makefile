.PHONY: all build lint test bench bench-compare bench-all bench-rust run clean

algo ?= builtin
size ?= 1000000
pattern ?= random
DATA := benches/data_$(size)_$(pattern).pkl
ITERS := $(shell python -c "print(max(10, 10000000 // $(size)))")

all: build lint test

build:
	python build_lib.py

lint:
	python lint.py

test:
	pytest tests/

$(DATA):
	python bench_hyperfine.py generate $(size) $(pattern) $(DATA)

bench: $(DATA)
	hyperfine --warmup 3 \
		"python bench_hyperfine.py run $(algo) $(DATA) --iters $(ITERS)"

bench-compare: $(DATA)
	hyperfine --warmup 3 --export-markdown benches/report.md \
		"python bench_hyperfine.py run smart $(DATA) --iters $(ITERS)" \
		"python bench_hyperfine.py run pdq $(DATA) --iters $(ITERS)" \
		"python bench_hyperfine.py run radix $(DATA) --iters $(ITERS)" \
		"python bench_hyperfine.py run builtin $(DATA) --iters $(ITERS)" \
		"python bench_hyperfine.py run par_sort_unstable $(DATA) --iters $(ITERS)"
	python benches/add_vs_builtin.py

bench-all:
	python bench_hyperfine.py generate 5000 random benches/data_5000_random.pkl
	hyperfine --warmup 3 \
		"python bench_hyperfine.py run bubble benches/data_5000_random.pkl" \
		"python bench_hyperfine.py run insertion benches/data_5000_random.pkl" \
		"python bench_hyperfine.py run merge benches/data_5000_random.pkl" \
		"python bench_hyperfine.py run quick benches/data_5000_random.pkl" \
		"python bench_hyperfine.py run heap benches/data_5000_random.pkl" \
		"python bench_hyperfine.py run intro benches/data_5000_random.pkl" \
		"python bench_hyperfine.py run tim benches/data_5000_random.pkl" \
		"python bench_hyperfine.py run pdq benches/data_5000_random.pkl" \
		"python bench_hyperfine.py run radix benches/data_5000_random.pkl" \
		"python bench_hyperfine.py run smart benches/data_5000_random.pkl" \
		"python bench_hyperfine.py run builtin benches/data_5000_random.pkl"

bench-rust:
	cargo bench

run:
	python run_examples.py

clean:
	python -c "import shutil, glob, os; [shutil.rmtree(p) for p in ['build', 'target', 'dist', '.pytest_cache', '.ruff_cache'] if os.path.exists(p)]; [os.remove(f) for f in glob.glob('benches/data_*.pkl') if os.path.exists(f)]"
