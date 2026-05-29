use numpy::PyArray1;
use pyo3::prelude::*;

#[pyfunction]
pub fn radix<'py>(_py: Python<'py>, arr: &PyArray1<i64>) -> PyResult<()> {
    let mut slice = unsafe { arr.as_array_mut() };
    radix_sort(slice.as_slice_mut().unwrap());
    Ok(())
}

pub fn radix_sort(arr: &mut [i64]) {
    let n = arr.len();
    if n <= 1 {
        return;
    }

    let min = *arr.iter().min().unwrap();
    let max = *arr.iter().max().unwrap();

    let abs_max = max.max(-min);

    if abs_max == 0 {
        return;
    }

    let mut neg: Vec<i64> = Vec::new();
    let mut pos: Vec<i64> = Vec::new();

    for &x in arr.iter() {
        if x < 0 {
            neg.push(-x);
        } else {
            pos.push(x);
        }
    }

    if !neg.is_empty() {
        radix_sort_unsigned(&mut neg);
        neg.reverse();
        for (i, val) in neg.iter().enumerate() {
            arr[i] = -*val;
        }
        let neg_len = neg.len();
        if !pos.is_empty() {
            radix_sort_unsigned(&mut pos);
            for (i, val) in pos.iter().enumerate() {
                arr[neg_len + i] = *val;
            }
        }
    } else {
        radix_sort_unsigned(arr);
    }
}

fn radix_sort_unsigned(arr: &mut [i64]) {
    let n = arr.len();
    if n <= 1 {
        return;
    }

    let max = *arr.iter().max().unwrap();
    if max == 0 {
        return;
    }

    let mut exp: i64 = 1;
    while max / exp > 0 {
        counting_sort(arr, exp);
        exp *= 10;
    }
}

fn counting_sort(arr: &mut [i64], exp: i64) {
    let n = arr.len();
    let mut output = vec![0i64; n];
    let mut count = [0usize; 10];

    for &val in arr.iter() {
        let digit = ((val / exp) % 10) as usize;
        count[digit] += 1;
    }

    for i in 1..10 {
        count[i] += count[i - 1];
    }

    for val in arr.iter().rev() {
        let digit = ((val / exp) % 10) as usize;
        output[count[digit] - 1] = *val;
        count[digit] -= 1;
    }

    arr.copy_from_slice(&output);
}
