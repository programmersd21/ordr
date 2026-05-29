use numpy::PyArray1;
use pyo3::prelude::*;

use crate::algorithms::heap::heapsort;
use crate::algorithms::insertion::insertion_sort;
use crate::algorithms::sorting_network::sort_small;

const INSERTION_CUTOFF: usize = 24;
const NINTHER_CUTOFF: usize = 128;
const MAX_DEPTH_FACTOR: usize = 48;

#[cfg(target_arch = "x86_64")]
#[inline(always)]
unsafe fn prefetch(addr: *const i64) {
    core::arch::x86_64::_mm_prefetch(addr as *const i8, core::arch::x86_64::_MM_HINT_T0);
}

#[cfg(not(target_arch = "x86_64"))]
#[inline(always)]
unsafe fn prefetch(_addr: *const i64) {}

#[pyfunction]
pub fn pdq<'py>(_py: Python<'py>, arr: &PyArray1<i64>) -> PyResult<()> {
    let mut slice = unsafe { arr.as_array_mut() };
    pdqsort(slice.as_slice_mut().unwrap());
    Ok(())
}

pub fn pdqsort(arr: &mut [i64]) {
    let n = arr.len();
    if n <= 1 {
        return;
    }
    let depth = n.next_power_of_two().trailing_zeros() as usize * MAX_DEPTH_FACTOR;
    pdqsort_impl(arr, depth);
}

fn pdqsort_impl(arr: &mut [i64], depth: usize) {
    let n = arr.len();

    if n <= INSERTION_CUTOFF {
        if n <= 4 {
            sort_small(arr);
        } else {
            insertion_sort(arr);
        }
        return;
    }

    if depth == 0 {
        heapsort(arr);
        return;
    }

    if is_sorted(arr) {
        return;
    }

    if is_reverse(arr) {
        arr.reverse();
        return;
    }

    let pivot = if n >= NINTHER_CUTOFF {
        ninther_pivot(arr)
    } else {
        median_of_three(arr)
    };

    let mid = hoare_partition(arr, pivot);

    if mid > 0 {
        pdqsort_impl(&mut arr[..mid], depth - 1);
    }
    if mid < n {
        pdqsort_impl(&mut arr[mid..], depth - 1);
    }
}

fn is_sorted(arr: &[i64]) -> bool {
    arr.windows(2).all(|w| w[0] <= w[1])
}

fn is_reverse(arr: &[i64]) -> bool {
    arr.windows(2).all(|w| w[0] >= w[1])
}

fn median_of_three(arr: &[i64]) -> i64 {
    let a = arr[0];
    let b = arr[arr.len() / 2];
    let c = arr[arr.len() - 1];
    if (a - b) * (c - a) >= 0 {
        a
    } else if (b - a) * (c - b) >= 0 {
        b
    } else {
        c
    }
}

fn ninther_pivot(arr: &[i64]) -> i64 {
    let third = arr.len() / 3;
    let s1 = median_of_three(&arr[..third]);
    let s2 = median_of_three(&arr[third..2 * third]);
    let s3 = median_of_three(&arr[2 * third..]);
    let candidates = [s1, s2, s3];
    let (a, b, c) = (candidates[0], candidates[1], candidates[2]);
    if (a - b) * (c - a) >= 0 {
        a
    } else if (b - a) * (c - b) >= 0 {
        b
    } else {
        c
    }
}

fn hoare_partition(arr: &mut [i64], pivot: i64) -> usize {
    let mut l = 0usize;
    let mut r = arr.len();
    loop {
        while l < r && arr[l] <= pivot {
            l += 1;
            if l + 12 < r {
                unsafe {
                    prefetch(&arr[l + 12]);
                }
            }
        }
        while l < r && arr[r - 1] > pivot {
            r -= 1;
            if r > 12 {
                unsafe {
                    prefetch(&arr[r - 13]);
                }
            }
        }
        if l >= r {
            break;
        }
        r -= 1;
        arr.swap(l, r);
        l += 1;
    }
    l
}
