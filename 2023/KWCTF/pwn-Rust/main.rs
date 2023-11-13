use std::io::{Write,stdin,stdout,BufRead};
use std::process::Command;

#[repr(C)]
struct Feedback {
    msg: [u8; 500],
    win: u64
}

fn input(prompt: &str) -> Vec<u8> {
    print!("{}",prompt);
    stdout().flush().unwrap();
    let mut buffer = Vec::new();
    stdin().lock().read_until(b'\n',&mut buffer).unwrap();
    // remove newline
    buffer.pop();
    buffer
}

fn main() {
    println!("What should I do with rust?");
    let comment: Vec<u8> = input("[*] Comment: ");
    let mut feedback = Feedback {
        msg: [0; 500],
        win: 0
    };
    unsafe {
        std::ptr::copy(comment.as_ptr(),feedback.msg.as_mut_ptr(),comment.len());
    }
    if feedback.win as usize <= 0 {
        println!("Thanks for your time");
    } else {
        Command::new("/bin/sh").status().expect("Error");
    }
}
