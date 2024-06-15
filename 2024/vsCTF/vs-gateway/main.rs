use std::io::{self, Write};
use std::process::{Command, self};
use std::fs;
use md5;
use rand::{self, Rng};

pub static mut ESSID: String = String::new();
static BSSID: &str = "94:4e:6f:d7:bf:05";
static mut BAND: String = String::new();
static mut CHANNEL: i32 = 0;
static mut WIFI_PASSWORD: String = String::new();
static mut ID: u64 = 0;

fn check_password(password: String) -> bool{
    let digest = md5::compute(password.trim());
    if format!("{:x}", digest) == "e10adc3949ba59abbe56e057f20f883e" {
        true
    }
    else{
        false
    }
}

fn auth() -> bool{
    let mut username = String::new();
    let mut password = String::new();

    print!("Username: ");
    io::stdout().flush().unwrap();
    io::stdin().read_line(&mut username).expect("Cannot read username!");
    
    print!("Password: ");
    io::stdout().flush().unwrap();
    io::stdin().read_line(&mut password).expect("Cannot read username!");

    if username.trim() == "admin" && check_password(password){
        println!("Access granted!");
        true
    }
    else{
        println!("Access forbidden!");
        false
    }
}

fn save_properties_to_file(){
    unsafe{
        let cmd = format!("echo \"{ESSID}\\n{BAND}\\n{CHANNEL}\\n{WIFI_PASSWORD}\" > /tmp/{ID}.conf");
        Command::new("/bin/sh")
                        .arg("-c")
                        .arg(cmd)
                        .output()
                        .expect("Failed to execute command");
    }
}

fn show_properties(){
    unsafe{
        println!("--- PROPERTIES -----------------------------");
        println!("Essid\t\t{ESSID}");
        println!("Bssid\t\t{BSSID}");
        println!("Band\t\t{BAND}GHz");
        println!("Channel\t\t{CHANNEL}");
        println!("Password\t{WIFI_PASSWORD}\n");
    }
}

fn change_essid(){
    let mut input: String = String::new();
    let mut done = false;

    unsafe{
        println!("Current essid: {ESSID}");
        while !done {
            done = true;
            print!("New essid: ");
            io::stdout().flush().unwrap();
            input.clear();
            io::stdin().read_line(&mut input).expect("Failed to readline");
            for c in input.trim().chars(){
                if !"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ".contains(c){
                    done = false;
                    break
                }
            }
        }
        ESSID = input.trim().to_owned();
        println!("Done!");
    }
    save_properties_to_file();
}

fn change_wifi_band(){
    unsafe{
        println!("Current band: {BAND}GHz");
        if BAND=="2.4"{
            BAND = String::from("5");
            CHANNEL = 100;
        }
        else{
            BAND = String::from("2.4");
            CHANNEL = 6;
        }
        println!("New band: {BAND}GHz");
    }
    save_properties_to_file();
}

fn change_channel(){
    let mut input: String = String::new();
    let mut channel_tmp: i32;

    unsafe{
        print!("Current band: {BAND}GHz ");
        if BAND == "2.4"{
            println!("(from 1 to 11)")
        }
        else{
            println!("(from 36 to 165)")
        }
        println!("Current channel: {CHANNEL}");
        loop {
            print!("New channel: ");
            io::stdout().flush().unwrap();
            input.clear();
            io::stdin().read_line(&mut input).expect("Failed to readline");
            channel_tmp = input.trim().parse().expect("Invalid number");
            if BAND == "2.4" && (1..12).contains(&channel_tmp){
                CHANNEL = channel_tmp;
                break;
            }
            else if BAND == "5" && (36..166).contains(&channel_tmp){
                CHANNEL = channel_tmp;
                break;
            }
        }
        println!("Done!\n");
    }
    save_properties_to_file();
}

fn change_wifi_password(){
    let mut input: String = String::new();

    unsafe{
        println!("Current password: {WIFI_PASSWORD}");
        print!("New password: ");
        io::stdout().flush().unwrap();
        input.clear();
        io::stdin().read_line(&mut input).expect("Failed to readline");
        WIFI_PASSWORD = input.trim().to_owned();
        println!("Done!");
    }
    save_properties_to_file();
}

fn menu(){
    println!("--- MENU ---------------------");
    println!("1. Show properties");
    println!("2. Change essid");
    println!("3. Change wifi band");
    println!("4. Change channel");
    println!("5. Change wifi password");
    println!("6. Exit");
    print!("> ");
    io::stdout().flush().unwrap();
}

fn load_data(){
    unsafe{
        ID = rand::thread_rng().gen_range(1..0xffffffffffffffff);

        let cmd = format!("echo \"View Source Guest\\n2.4\\n6\\n123456789\" > /tmp/{ID}.conf");
        Command::new("/bin/sh")
                        .arg("-c")
                        .arg(cmd)
                        .output()
                        .expect("Failed to execute command");

        let datas = fs::read_to_string(format!("/tmp/{ID}.conf")).expect("Cannot load default data");
        let mut parts = datas.split("\n");
        ESSID   = parts.nth(0).expect("Error when parsing essid").to_owned();
        BAND    = parts.nth(0).expect("Error when parsing band").to_owned();
        CHANNEL = parts.nth(0).expect("Error when parsing channel").to_owned().parse().unwrap();
        WIFI_PASSWORD = parts.nth(0).expect("Error when parsing wifi password").to_owned();
    }
}

fn run(){
    let mut choice;
    let mut input = String::new();

    load_data();
    show_properties();
    loop {
        menu();
        input.clear();
        io::stdin().read_line(&mut input).expect("Cannot read input!");
        choice = match input.trim().parse() {
            Ok(num) => num,
            _ => 0
        };
        match choice {
            1 => show_properties(),
            2 => change_essid(),
            3 => change_wifi_band(),
            4 => change_channel(),
            5 => change_wifi_password(),
            6 => {
                unsafe{
                    fs::remove_file(format!("/tmp/{ID}.conf")).unwrap();
                }
                break
            },
            _ => {
                println!("Invalid choice!");
            },
        }
    }
}

fn main() {
    println!("----------------------------");
    println!("|        VS Gateway        |");
    println!("----------------------------");

    if auth(){
        run();
    }
    process::exit(0);
}