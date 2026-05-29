use numpy::PyArray1;
use pyo3::prelude::*;

use crate::algorithms::heap::heapsort;
use crate::algorithms::insertion::insertion_sort;

const INSERTION_CUTOFF: usize = 16;

pub fn introsort(arr: &mut [i64]) {
    let n = arr.len();
    if n > 1 {
        let depth_limit = (2.0 * (n as f64).log2()) as usize;
        introsort_impl(arr, 0, n - 1, depth_limit);
    }
}

#[pyfunction]
pub fn intro<'py>(_py: Python<'py>, arr: &PyArray1<i64>) -> PyResult<()> {
    let mut slice = unsafe { arr.as_array_mut() };
    introsort(slice.as_slice_mut().unwrap());
    Ok(())
}

fn introsort_impl(arr: &mut [i64], low: usize, high: usize, depth_limit: usize) {
    let size = high - low + 1;

    if size <= INSERTION_CUTOFF {
        insertion_sort(&mut arr[low..=high]);
        return;
    }

    if depth_limit == 0 {
        heapsort(&mut arr[low..=high]);
        return;
    }

    let p = partition(arr, low, high);
    if p > 0 {
        introsort_impl(arr, low, p - 1, depth_limit - 1);
    }
    introsort_impl(arr, p + 1, high, depth_limit - 1);
}

fn partition(arr: &mut [i64], low: usize, high: usize) -> usize {
    let pivot = arr[high];
    let mut i = low;
    for j in low..high {
        if arr[j] <= pivot {
            arr.swap(i, j);
            i += 1;
        }
    }
    arr.swap(i, high);
    i
}
