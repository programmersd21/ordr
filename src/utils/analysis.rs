use std::collections::HashSet;

const SAMPLE_SIZE: usize = 100;

pub fn measure_presortedness(arr: &[i64]) -> f64 {
    let len = arr.len();
    if len <= 1 {
        return 1.0;
    }

    let sample_size = len.min(SAMPLE_SIZE);
    let step = if len > sample_size {
        len / sample_size
    } else {
        1
    };

    let mut inversions = 0;
    let mut comparisons = 0;

    for i in (0..len).step_by(step).take(sample_size) {
        for j in (i + step..len).step_by(step).take(sample_size - i / step) {
            if arr[i] > arr[j] {
                inversions += 1;
            }
            comparisons += 1;
        }
    }

    if comparisons == 0 {
        return 1.0;
    }

    1.0 - (inversions as f64 / comparisons as f64)
}

pub fn measure_duplicate_ratio(arr: &[i64]) -> f64 {
    let len = arr.len();
    if len <= 1 {
        return 0.0;
    }

    let sample_size = len.min(SAMPLE_SIZE);
    let step = if len > sample_size {
        len / sample_size
    } else {
        1
    };

    let mut seen = HashSet::new();
    let mut total = 0;
    let mut duplicates = 0;

    for i in (0..len).step_by(step).take(sample_size) {
        total += 1;
        if !seen.insert(arr[i]) {
            duplicates += 1;
        }
    }

    if total == 0 {
        return 0.0;
    }

    duplicates as f64 / total as f64
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_presortedness_sorted() {
        let arr = vec![1, 2, 3, 4, 5];
        assert!(measure_presortedness(&arr) > 0.95);
    }

    #[test]
    fn test_presortedness_reverse() {
        let arr = vec![5, 4, 3, 2, 1];
        assert!(measure_presortedness(&arr) < 0.1);
    }

    #[test]
    fn test_duplicate_ratio_all_same() {
        let arr = vec![5, 5, 5, 5, 5];
        assert!(measure_duplicate_ratio(&arr) > 0.7);
    }

    #[test]
    fn test_duplicate_ratio_unique() {
        let arr = vec![1, 2, 3, 4, 5];
        assert!(measure_duplicate_ratio(&arr) < 0.1);
    }
}
