use std::io::Read;
use regex::Regex;
use sha2::{Sha256, Digest};

#[allow(dead_code)]
/// Hack
///
///     use std::fs::File;
///     use std::io::Read;
///     let mut file_handle = File::open("flag.txt".to_string()).expect("Flag file not found!");
///     let mut flag = String::new();
///
///     file_handle
///           .read_to_string(&mut flag)
///           .expect("Can't read file");
///
///     assert!(false, "{}", flag);
fn validate_flag(flag: &str) -> bool {
    let flag_pattern = Regex::new(r"^COMPFEST16\{.*\}$").unwrap();
    if !flag_pattern.is_match(flag) {
        println!("1");
        return false;
    }

    let flag_len = flag.len();
    if flag_len < 12 {
        println!("2");
        return false;
    }

    let last_10_chars = &flag[flag_len - 11..flag_len - 1];

    let content_start = flag.find('{').unwrap() + 1;
    let content_end = flag_len - 12;
    let content_before_last_10 = &flag[content_start..content_end];

    let mut hasher = Sha256::new();
    hasher.update(content_before_last_10);
    let result = hasher.finalize();

    let hashed_string = format!("{:x}", result);
    let first_10_hashed_chars = &hashed_string[..10];

    last_10_chars == first_10_hashed_chars
}

#[cfg(test)]
mod tests {
    use super::*;
    const PATH_TO_FLAG: &str = "resources/flag.txt";

    #[test]
    fn test_valid_flag() {
        let mut file_open = std::fs::File::open(PATH_TO_FLAG).expect("Flag file not found.");
        let mut flag_string = String::new();
        file_open.read_to_string(&mut flag_string).expect("File can't be read");
        assert!(validate_flag(&flag_string));
    }
}

