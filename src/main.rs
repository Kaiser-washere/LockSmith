// crack.rs — unified Rust module for long wordlists
// Build: cargo build --release; copy target/release/crack_rs
use clap::{Arg, Command};
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::process::{Command as PCommand, exit};

// progress bar helper
fn progress_bar(done: usize, total: usize) -> String {
    let width = 30usize;
    let total = if total == 0 { 1 } else { total };
    let ratio = (done as f64) / (total as f64);
    let fill = (ratio * (width as f64)).round() as usize;
    let fill = fill.min(width);
    let bar = format!("{}{}", "█".repeat(fill), "▒".repeat(width - fill));
    format!("\x1b[36m\x1b[1m[{}] {}/{} ({:.1}%)\x1b[0m", bar, done, total, ratio * 100.0)
}

// format-specific password attempts
fn try_zip(_archive: &str, _password: &str) -> bool {
    // TODO: integrate encrypted ZIP crate
    false
}

fn try_rar(archive: &str, password: &str) -> bool {
    let status = PCommand::new("unrar")
        .arg("t")
        .arg(format!("-p{}", password))
        .arg("-y")
        .arg(archive)
        .status();
    matches!(status, Ok(s) if s.success())
}

fn try_7z(archive: &str, password: &str) -> bool {
    let status = PCommand::new("7z")
        .arg("t")
        .arg(format!("-p{}", password))
        .arg(archive)
        .status();
    matches!(status, Ok(s) if s.success())
}

fn try_placeholder(_archive: &str, _password: &str) -> bool {
    false
}

fn main() {
    let matches = Command::new("crack_rs")
        .arg(Arg::new("format").long("format").required(true))
        .arg(Arg::new("archive").long("archive").required(true))
        .arg(Arg::new("wordlist").long("wordlist").required(true))
        .arg(Arg::new("total").long("total").required(true))
        .get_matches();

    let format = matches.get_one::<String>("format").unwrap();
    let archive = matches.get_one::<String>("archive").unwrap();
    let wordlist = matches.get_one::<String>("wordlist").unwrap();
    let total = matches.get_one::<String>("total").unwrap().parse::<usize>().unwrap_or(0);

    let file = File::open(wordlist).expect("Cannot open wordlist");
    let reader = BufReader::new(file);

    let mut done: usize = 0;
    for line in reader.lines() {
        let pw = line.unwrap_or_default().trim().to_string();
        done += 1;
        let ok = match format.as_str() {
            "zip" => try_zip(archive, &pw),
            "rar" => try_rar(archive, &pw),
            "7z" => try_7z(archive, &pw),
            "targz" | "bz2" | "gz" | "lzma" => try_placeholder(archive, &pw),
            _ => { eprintln!("\x1b[31mUnsupported format\x1b[0m"); exit(2); }
        };
        if ok {
            println!("\n\x1b[32m\x1b[1m[+] Password found:\x1b[0m {}", pw);
            exit(0);
        } else {
            println!("{}  try: {}", progress_bar(done, total), pw);
        }
    }
    println!("\n\x1b[31m[-] Password not found in wordlist.\x1b[0m");
    exit(1);
}
