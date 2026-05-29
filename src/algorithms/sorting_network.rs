#[inline(always)]
fn cmp_swap(arr: &mut [i64], i: usize, j: usize) {
    if arr[i] > arr[j] {
        arr.swap(i, j);
    }
}

/// Verified optimal sorting networks for n=2,3,4.
/// For n>4, caller should use insertion_sort instead.
pub fn sort_small(arr: &mut [i64]) {
    let n = arr.len();
    match n {
        0 | 1 => {}
        2 => cmp_swap(arr, 0, 1),
        3 => {
            cmp_swap(arr, 0, 2);
            cmp_swap(arr, 0, 1);
            cmp_swap(arr, 1, 2);
        }
        4 => {
            cmp_swap(arr, 0, 2);
            cmp_swap(arr, 1, 3);
            cmp_swap(arr, 0, 1);
            cmp_swap(arr, 2, 3);
            cmp_swap(arr, 1, 2);
        }
        _ => {}
    }
}
