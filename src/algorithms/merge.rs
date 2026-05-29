use numpy::PyArray1;
use pyo3::prelude::*;

#[pyfunction]
pub fn merge<'py>(_py: Python<'py>, arr: &PyArray1<i64>) -> PyResult<()> {
    let mut slice = unsafe { arr.as_array_mut() };
    merge_sort_inplace(slice.as_slice_mut().unwrap());
    Ok(())
}

pub fn merge_sort_inplace(arr: &mut [i64]) {
    let n = arr.len();
    if n <= 1 {
        return;
    }
    let mut temp = vec![0i64; n];
    merge_sort(arr, &mut temp, 0, n);
}

fn merge_sort(arr: &mut [i64], temp: &mut [i64], left: usize, right: usize) {
    if right - left <= 1 {
        return;
    }
    let mid = left + (right - left) / 2;
    merge_sort(arr, temp, left, mid);
    merge_sort(arr, temp, mid, right);
    merge_halves(arr, temp, left, mid, right);
}

fn merge_halves(arr: &mut [i64], temp: &mut [i64], left: usize, mid: usize, right: usize) {
    let mut i = left;
    let mut j = mid;
    let mut k = left;

    while i < mid && j < right {
        if arr[i] <= arr[j] {
            temp[k] = arr[i];
            i += 1;
        } else {
            temp[k] = arr[j];
            j += 1;
        }
        k += 1;
    }

    while i < mid {
        temp[k] = arr[i];
        i += 1;
        k += 1;
    }

    while j < right {
        temp[k] = arr[j];
        j += 1;
        k += 1;
    }

    arr[left..right].copy_from_slice(&temp[left..right]);
}
