use numpy::PyArray1;
use pyo3::prelude::*;

use crate::algorithms::insertion::insertion_sort;
use crate::algorithms::pdq::pdqsort;
use crate::algorithms::radix::radix_sort;
use crate::algorithms::tim::timsort;
use crate::parallel::par_merge::par_sort_unstable_impl;
use crate::utils::analysis::{measure_duplicate_ratio, measure_presortedness};

const SMALL_THRESHOLD: usize = 16;
const LARGE_THRESHOLD: usize = 100_000;
const HIGH_PRESORTEDNESS: f64 = 0.9;
const HIGH_DUPLICATE_RATIO: f64 = 0.5;
const RADIX_MIN_SIZE: usize = 1000;
const RADIX_MAX_RANGE: i64 = 1_000_000;

pub fn smart_sort(arr: &mut [i64]) {
    let n = arr.len();
    if n <= 1 {
        return;
    }
    if n <= SMALL_THRESHOLD {
        insertion_sort(arr);
        return;
    }

    let presortedness = measure_presortedness(arr);
    let duplicate_ratio = measure_duplicate_ratio(arr);

    if presortedness > HIGH_PRESORTEDNESS {
        timsort(arr);
        return;
    }

    if duplicate_ratio > HIGH_DUPLICATE_RATIO {
        timsort(arr);
        return;
    }

    if n > LARGE_THRESHOLD {
        par_sort_unstable_impl(arr);
        return;
    }

    if n >= RADIX_MIN_SIZE && is_radix_suitable(arr) {
        radix_sort(arr);
        return;
    }

    pdqsort(arr);
}

fn is_radix_suitable(arr: &[i64]) -> bool {
    let sample_size = arr.len().min(1000);
    let step = arr.len() / sample_size;

    let mut min = i64::MAX;
    let mut max = i64::MIN;

    for i in (0..arr.len()).step_by(step).take(sample_size) {
        let val = arr[i];
        if val < min {
            min = val;
        }
        if val > max {
            max = val;
        }
    }

    max - min < RADIX_MAX_RANGE
}

#[pyfunction]
pub fn smart<'py>(_py: Python<'py>, arr: &PyArray1<i64>) -> PyResult<()> {
    let mut slice = unsafe { arr.as_array_mut() };
    smart_sort(slice.as_slice_mut().unwrap());
    Ok(())
}
