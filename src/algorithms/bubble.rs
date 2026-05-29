use numpy::PyArray1;
use pyo3::prelude::*;

#[pyfunction]
pub fn bubble<'py>(_py: Python<'py>, arr: &PyArray1<i64>) -> PyResult<()> {
    let mut slice = unsafe { arr.as_array_mut() };
    bubble_sort(slice.as_slice_mut().unwrap());
    Ok(())
}

pub fn bubble_sort(arr: &mut [i64]) {
    let n = arr.len();
    if n <= 1 {
        return;
    }
    for i in 0..n {
        let mut swapped = false;
        for j in 0..n - i - 1 {
            if arr[j] > arr[j + 1] {
                arr.swap(j, j + 1);
                swapped = true;
            }
        }
        if !swapped {
            break;
        }
    }
}
