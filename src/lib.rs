use pyo3::prelude::*;

pub mod adaptive;
pub mod algorithms;
pub mod parallel;
pub mod utils;

#[global_allocator]
static GLOBAL_ALLOCATOR: mimalloc::MiMalloc = mimalloc::MiMalloc;

#[pymodule]
fn _ordr(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(algorithms::bubble::bubble, m)?)?;
    m.add_function(wrap_pyfunction!(algorithms::insertion::insertion, m)?)?;
    m.add_function(wrap_pyfunction!(algorithms::merge::merge, m)?)?;
    m.add_function(wrap_pyfunction!(algorithms::quick::quick, m)?)?;
    m.add_function(wrap_pyfunction!(algorithms::heap::heap, m)?)?;
    m.add_function(wrap_pyfunction!(algorithms::intro::intro, m)?)?;
    m.add_function(wrap_pyfunction!(algorithms::tim::tim, m)?)?;
    m.add_function(wrap_pyfunction!(algorithms::pdq::pdq, m)?)?;
    m.add_function(wrap_pyfunction!(algorithms::radix::radix, m)?)?;
    m.add_function(wrap_pyfunction!(adaptive::smart::smart, m)?)?;
    m.add_function(wrap_pyfunction!(parallel::par_merge::par_sort, m)?)?;
    m.add_function(wrap_pyfunction!(parallel::par_merge::par_sort_unstable, m)?)?;
    m.add_function(wrap_pyfunction!(parallel::par_merge::par_merge, m)?)?;

    Ok(())
}
