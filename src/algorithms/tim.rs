use numpy::PyArray1;
use pyo3::prelude::*;

use crate::algorithms::insertion::insertion_sort;

const MIN_MERGE: usize = 32;

#[pyfunction]
pub fn tim<'py>(_py: Python<'py>, arr: &PyArray1<i64>) -> PyResult<()> {
    let mut slice = unsafe { arr.as_array_mut() };
    timsort(slice.as_slice_mut().unwrap());
    Ok(())
}

pub fn timsort(arr: &mut [i64]) {
    let n = arr.len();
    if n <= 1 {
        return;
    }
    let min_run = compute_min_run(n);

    let mut i = 0;
    while i < n {
        let run_end = (i + min_run - 1).min(n - 1);
        insertion_sort(&mut arr[i..=run_end]);
        i = run_end + 1;
    }

    let mut size = min_run;
    while size < n {
        let mut left = 0;
        while left < n {
            let mid = left + size;
            if mid >= n {
                break;
            }
            let right = (left + 2 * size).min(n);
            let mut merged = arr[left..right].to_vec();
            merge_halves(&mut merged, size, right - left);
            arr[left..right].copy_from_slice(&merged);
            left = right;
        }
        size *= 2;
    }
}

fn compute_min_run(n: usize) -> usize {
    let mut r = 0;
    let mut len = n;
    while len >= MIN_MERGE {
        r |= len & 1;
        len >>= 1;
    }
    len + r
}

fn merge_halves(arr: &mut [i64], split: usize, total: usize) {
    let left = arr[..split].to_vec();
    let right = arr[split..total].to_vec();

    let mut i = 0;
    let mut j = 0;
    let mut k = 0;

    while i < left.len() && j < right.len() {
        if left[i] <= right[j] {
            arr[k] = left[i];
            i += 1;
        } else {
            arr[k] = right[j];
            j += 1;
        }
        k += 1;
    }

    while i < left.len() {
        arr[k] = left[i];
        i += 1;
        k += 1;
    }

    while j < right.len() {
        arr[k] = right[j];
        j += 1;
        k += 1;
    }
}
