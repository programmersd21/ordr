use numpy::PyArray1;
use pyo3::prelude::*;
use rayon::prelude::*;

#[pyfunction]
pub fn par_sort<'py>(_py: Python<'py>, arr: &PyArray1<i64>) -> PyResult<()> {
    let mut slice = unsafe { arr.as_array_mut() };
    slice.as_slice_mut().unwrap().par_sort();
    Ok(())
}

#[pyfunction]
pub fn par_sort_unstable<'py>(_py: Python<'py>, arr: &PyArray1<i64>) -> PyResult<()> {
    let mut slice = unsafe { arr.as_array_mut() };
    par_sort_unstable_impl(slice.as_slice_mut().unwrap());
    Ok(())
}

pub fn par_sort_unstable_impl(arr: &mut [i64]) {
    arr.par_sort_unstable();
}

#[pyfunction]
pub fn par_merge<'py>(_py: Python<'py>, arr: &PyArray1<i64>) -> PyResult<()> {
    let mut slice = unsafe { arr.as_array_mut() };
    let a = slice.as_slice_mut().unwrap();
    let n = a.len();
    if n > 1 {
        par_merge_sort(a);
    }
    Ok(())
}

fn par_merge_sort(arr: &mut [i64]) {
    let n = arr.len();
    if n <= 1 {
        return;
    }

    if n < 8192 {
        arr.sort();
        return;
    }

    let mid = n / 2;
    let (left, right) = arr.split_at_mut(mid);

    rayon::join(|| par_merge_sort(left), || par_merge_sort(right));

    let mut merged = arr.to_vec();
    let mut i = 0;
    let mut j = mid;
    let mut k = 0;

    while i < mid && j < n {
        if arr[i] <= arr[j] {
            merged[k] = arr[i];
            i += 1;
        } else {
            merged[k] = arr[j];
            j += 1;
        }
        k += 1;
    }

    while i < mid {
        merged[k] = arr[i];
        i += 1;
        k += 1;
    }

    while j < n {
        merged[k] = arr[j];
        j += 1;
        k += 1;
    }

    arr.copy_from_slice(&merged);
}
