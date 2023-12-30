use std::{io::{Write, stdin, stdout, BufRead}, process::exit};

#[repr(C)]
struct Pwnable {
    data: [u8; 500],
    win: u64
}

fn input(prompt: &str) -> Vec<u8> {
    print!("{}", prompt);
    stdout().flush().unwrap();
    let mut buffer = Vec::new();
    stdin().lock().read_until(b'\n', &mut buffer).unwrap();
    buffer
}

fn read_flag(){
    let flag = std::fs::read_to_string("flag.txt");
    match flag {
        Ok(flag) => println!("{}", flag),
        Err(_) => println!("flag not found")
    }
}
fn main() {
    println!("wat sud i do wit rust?");
    let buf: Vec<u8> = input("> ");
    let mut pwn = Pwnable {
        data: [0; 500],
        win: 0
    };
    unsafe { std::ptr::copy(buf.as_ptr(), pwn.data.as_mut_ptr(), buf.len()) }
    if pwn.win as usize == 0xdeadb19b00b5dead {
        read_flag();
        exit(0);
    } else {
        println!("nope");
        exit(1);
    }
}