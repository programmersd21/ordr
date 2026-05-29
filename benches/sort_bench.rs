use criterion::{black_box, criterion_group, criterion_main, BenchmarkId, Criterion};
use ordr::adaptive::smart::smart_sort;
use ordr::algorithms::{intro::introsort, pdq::pdqsort, quick::quicksort, tim::timsort};
use ordr::parallel::par_merge::par_sort_unstable_impl;

fn generate_random(size: usize) -> Vec<i64> {
    (0..size)
        .map(|i| ((i * 2654435761) % size) as i64)
        .collect()
}

fn generate_sorted(size: usize) -> Vec<i64> {
    (0..size as i64).collect()
}

fn generate_reverse(size: usize) -> Vec<i64> {
    (0..size as i64).rev().collect()
}

fn generate_nearly_sorted(size: usize) -> Vec<i64> {
    let mut arr: Vec<i64> = (0..size as i64).collect();
    for i in (0..size / 10).step_by(10) {
        if i + 1 < size {
            arr.swap(i, i + 1);
        }
    }
    arr
}

fn bench_algorithms(c: &mut Criterion) {
    let sizes = vec![100, 1000, 10000];

    for size in sizes {
        let mut group = c.benchmark_group(format!("random_{}", size));
        let data = generate_random(size);

        group.bench_with_input(BenchmarkId::new("smart", size), &data, |b, d| {
            b.iter(|| smart_sort(&mut black_box(d.clone())))
        });

        group.bench_with_input(BenchmarkId::new("pdq", size), &data, |b, d| {
            b.iter(|| pdqsort(&mut black_box(d.clone())))
        });

        group.bench_with_input(BenchmarkId::new("intro", size), &data, |b, d| {
            b.iter(|| introsort(&mut black_box(d.clone())))
        });

        group.bench_with_input(BenchmarkId::new("tim", size), &data, |b, d| {
            b.iter(|| timsort(&mut black_box(d.clone())))
        });

        group.bench_with_input(BenchmarkId::new("quick", size), &data, |b, d| {
            b.iter(|| quicksort(&mut black_box(d.clone())))
        });

        group.finish();
    }
}

fn bench_patterns(c: &mut Criterion) {
    let size = 10000;

    let mut group = c.benchmark_group("patterns");

    let sorted = generate_sorted(size);
    group.bench_function("sorted_smart", |b| {
        b.iter(|| smart_sort(&mut black_box(sorted.clone())))
    });

    let reverse = generate_reverse(size);
    group.bench_function("reverse_smart", |b| {
        b.iter(|| smart_sort(&mut black_box(reverse.clone())))
    });

    let nearly = generate_nearly_sorted(size);
    group.bench_function("nearly_sorted_smart", |b| {
        b.iter(|| smart_sort(&mut black_box(nearly.clone())))
    });

    group.finish();
}

fn bench_parallel(c: &mut Criterion) {
    let sizes = vec![10000, 100000];

    for size in sizes {
        let mut group = c.benchmark_group(format!("parallel_{}", size));
        let data = generate_random(size);

        group.bench_with_input(BenchmarkId::new("par_sort", size), &data, |b, d| {
            b.iter(|| par_sort_unstable_impl(&mut black_box(d.clone())))
        });

        group.bench_with_input(BenchmarkId::new("pdq", size), &data, |b, d| {
            b.iter(|| pdqsort(&mut black_box(d.clone())))
        });

        group.finish();
    }
}

criterion_group!(benches, bench_algorithms, bench_patterns, bench_parallel);
criterion_main!(benches);
