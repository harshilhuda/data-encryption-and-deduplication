use aes_gcm::{
    aead::{Aead, AeadCore, KeyInit, OsRng},
    Aes256Gcm, Nonce, Key // Or `Aes128Gcm`
};
use aes_gcm::aead::{generic_array::GenericArray};
use std::fs::{File, OpenOptions};
use std::io::{BufReader, Read, Write};
use sha2::{Sha256, Digest};

const NONCE_SIZE: usize = 12;

pub fn derive_aes_key(password: &str) -> [u8; 32] {
    let mut hasher = Sha256::new();
    hasher.update(password);
    let result = hasher.finalize();
    
    let mut key = [0u8; 32];
    key.copy_from_slice(&result[..]);
    
    key
}

pub fn encrypt(input_path: &str, output_path: &str, password: &str) -> String {
    let mut input_file = File::open(input_path).unwrap();
    let mut output_file = OpenOptions::new().write(true).create_new(true).open(output_path).unwrap();

    let mut buffer = Vec::new();
    input_file.read_to_end(&mut buffer).unwrap();

    let key = &derive_aes_key(password);
    let key: &Key<Aes256Gcm> = key.into();

    let cipher = Aes256Gcm::new(&key);
    let nonce = Aes256Gcm::generate_nonce(&mut OsRng); // 96-bits; unique per message
    
    let ciphertext = cipher.encrypt(GenericArray::from_slice(&nonce), buffer.as_slice()).unwrap();
    
    output_file.write_all(&nonce).unwrap();
    output_file.write_all(&ciphertext).unwrap();

    return "Success".to_string();
}

pub fn decrypt(input_path: &str, output_path: &str, password: &str) -> String {
    let mut input_file = File::open(input_path).unwrap();
    let mut output_file = OpenOptions::new().write(true).create_new(true).open(output_path).unwrap();

    let key = &derive_aes_key(password);
    let key: &Key<Aes256Gcm> = key.into();

    // Read nonce from input file
    let mut nonce = [0u8; NONCE_SIZE];
    input_file.read_exact(&mut nonce).unwrap();

    // Read ciphertext from input file
    let mut ciphertext = Vec::new();
    input_file.read_to_end(&mut ciphertext).unwrap();

    // Create AES-GCM cipher instance with provided key
    let cipher = Aes256Gcm::new(key.into());

    // Decrypt ciphertext
    let plaintext = cipher.decrypt(&nonce.into(), ciphertext.as_ref()).unwrap();

    // Write decrypted plaintext to output file
    output_file.write_all(&plaintext).unwrap();

    return "Success".to_string();
}
