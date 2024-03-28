mod encrypt;
mod hash;

use encrypt::{encrypt, decrypt};
use std::fs::File;
use std::io::{BufReader, Read};
use pyo3::prelude::*;
use blake3::Hasher;
/// Formats the sum of two numbers as string.
#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

#[pyfunction]
fn calculate_file_hash(_py: Python, filename: &str) -> PyResult<String> {
    hash::calculate_time(filename);
    
    let mut hasher = Hasher::new();
    let mut reader = BufReader::new(File::open(filename)?);

    let mut buf = [0; 4096];
    
    loop {
        let bytes_read = reader.read(&mut buf)?;
        if bytes_read == 0 {
            break;
        }
        hasher.update(&buf[..bytes_read]);
    }

    Ok(hasher.finalize().to_string())
}

#[pyfunction]
fn encrypt_file(_py: Python, input_file: &str, output_file: &str, key: &str) -> PyResult<String> {
    Ok(encrypt(input_file, output_file, key).to_string())
}

#[pyfunction]
fn decrypt_file(_py: Python, input_file: &str, output_file: &str, key: &str) -> PyResult<String> {
    Ok(decrypt(input_file, output_file, key).to_string())
}

/// A Python module implemented in Rust.
#[pymodule]
fn rust_hash_module(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(calculate_file_hash, m)?)?;
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    m.add_function(wrap_pyfunction!(encrypt_file, m)?)?;
    m.add_function(wrap_pyfunction!(decrypt_file, m)?)?;
    Ok(())
}
