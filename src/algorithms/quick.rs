use numpy::PyArray1;
use pyo3::prelude::*;

pub fn quicksort(arr: &mut [i64]) {
    let n = arr.len();
    if n > 1 {
        quicksort_impl(arr, 0, n - 1);
    }
}

#[pyfunction]
pub fn quick<'py>(_py: Python<'py>, arr: &PyArray1<i64>) -> PyResult<()> {
    let mut slice = unsafe { arr.as_array_mut() };
    quicksort(slice.as_slice_mut().unwrap());
    Ok(())
}

fn quicksort_impl(arr: &mut [i64], low: usize, high: usize) {
    if low >= high {
        return;
    }
    let p = partition(arr, low, high);
    if p > 0 {
        quicksort_impl(arr, low, p - 1);
    }
    quicksort_impl(arr, p + 1, high);
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
