use numpy::PyArray1;
use pyo3::prelude::*;

#[pyfunction]
pub fn insertion<'py>(_py: Python<'py>, arr: &PyArray1<i64>) -> PyResult<()> {
    let mut slice = unsafe { arr.as_array_mut() };
    insertion_sort(slice.as_slice_mut().unwrap());
    Ok(())
}

pub fn insertion_sort(arr: &mut [i64]) {
    let n = arr.len();
    if n <= 1 {
        return;
    }
    for i in 1..n {
        let key = arr[i];
        let mut j = i;
        while j > 0 && arr[j - 1] > key {
            arr[j] = arr[j - 1];
            j -= 1;
        }
        arr[j] = key;
    }
}
