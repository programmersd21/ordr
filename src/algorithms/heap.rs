use numpy::PyArray1;
use pyo3::prelude::*;

#[pyfunction]
pub fn heap<'py>(_py: Python<'py>, arr: &PyArray1<i64>) -> PyResult<()> {
    let mut slice = unsafe { arr.as_array_mut() };
    heapsort(slice.as_slice_mut().unwrap());
    Ok(())
}

pub fn heapsort(arr: &mut [i64]) {
    let n = arr.len();
    if n <= 1 {
        return;
    }
    for i in (0..n / 2).rev() {
        sift_down(arr, i, n);
    }
    for i in (1..n).rev() {
        arr.swap(0, i);
        sift_down(arr, 0, i);
    }
}

fn sift_down(arr: &mut [i64], start: usize, end: usize) {
    let mut root = start;
    loop {
        let child = 2 * root + 1;
        if child >= end {
            break;
        }
        let mut swap = root;
        if arr[swap] < arr[child] {
            swap = child;
        }
        if child + 1 < end && arr[swap] < arr[child + 1] {
            swap = child + 1;
        }
        if swap == root {
            break;
        }
        arr.swap(root, swap);
        root = swap;
    }
}
