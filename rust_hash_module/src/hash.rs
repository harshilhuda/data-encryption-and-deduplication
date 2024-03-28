use blake3::Hasher;
use chksum_md5 as md5;
use sha2::{Digest, Sha256};
use std::fs::File;
use std::io::{BufReader, Error, Read};
use std::time::Instant;

pub fn calculate_time(filename: &str){
    let before_blake3 = Instant::now();
    calculate_file_hash_blake3(filename);
    let after_blake3 = Instant::now();
    let elapsed_time = after_blake3.duration_since(before_blake3);
    println!("Elapsed time Blake3: {:?}", elapsed_time);

    let before_md5 = Instant::now();
    calculate_file_hash_md5(filename);
    let after_md5 = Instant::now();
    let elapsed_time = after_md5.duration_since(before_md5);
    println!("Elapsed time MD5: {:?}", elapsed_time);
    
    let before_sha256 = Instant::now();
    calculate_file_hash_sha256(filename);
    let after_sha256 = Instant::now();
    let elapsed_time = after_sha256.duration_since(before_sha256);
    println!("Elapsed time Sha256: {:?}", elapsed_time);
}

fn calculate_file_hash_blake3(filename: &str) -> String {
    let mut hasher = Hasher::new();
    let mut reader = BufReader::new(File::open(filename).unwrap());

    let mut buf = [0; 4096];
    
    loop {
        let bytes_read = reader.read(&mut buf).unwrap();
        if bytes_read == 0 {
            break;
        }
        hasher.update(&buf[..bytes_read]);
    }

    hasher.finalize().to_string()
}

fn calculate_file_hash_md5(filename: &str) -> String {
    let mut reader = File::open(filename).unwrap();

    let digest = md5::chksum(reader).unwrap();

    digest.to_hex_lowercase()
}

fn calculate_file_hash_sha256(filename: &str) -> String {
    let mut hasher = Sha256::new();
    let mut reader = BufReader::new(File::open(filename).unwrap());

    let mut buf = [0; 4096];
    
    loop {
        let bytes_read = reader.read(&mut buf).unwrap();
        if bytes_read == 0 {
            break;
        }
        hasher.update(&buf[..bytes_read]);
    }

    let digest = hasher.finalize();
    
    format!("{:x}", digest)
}