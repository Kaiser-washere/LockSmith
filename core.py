#!/usr/bin/env python3
# LockSmith — Core CLI (unified)
# Tek binary: crack_go (short wordlist), crack_rs (long wordlist)

import os
import sys
import subprocess
import shutil
from datetime import datetime

# ANSI colors
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"

ASCII = f"""{MAGENTA}{BOLD}
⠀⠀⠀⠀⠀⠀⡤⡀⠠⡀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⠆⣸⠃⠊⠭⠂⣠⠀
⠀⠀⠀⠀⢠⠃⡐⠃⠀⠀⠀⡌⠱⡀
⠀⠀⠀⠀⠰⡀⡄⠀⠀⠀⡜⢀⠒⠁
⠀⠀⠀⠀⠀⢈⡟⢔⠒⣈⠔⠁⠀⠀
⠀⠀⠀⠀⠀⡼⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠰⠇⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢰⠀⠀⢀⢱⠀⠀⠀⠀⠀
⠶⡤⠄⡀⢸⠀⣠⢊⡌⠀⠀⠀⠀⠀
⠀⠈⠄⠈⢢⠊⡡⠋⠀⠀⠀⠀⠀⠀
⠀⠀⠸⠀⠀⢠⠁⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠡⡈⢜⡀⣀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠈⠒⠓⠃⠀⠀⠀⠀⠀⠀
{RESET}"""

TITLE = f"{BOLD}{CYAN}LockSmith — Archive Password Recovery (legal use only){RESET}"

FORMATS = {
    "1": "zip",
    "2": "rar",
    "3": "targz",
    "4": "7z",
    "5": "bz2",
    "6": "gz",
    "7": "lzma",
}

WORDLIST_THRESHOLD = 1000  # <1000 lines → Go, >=1000 lines → Rust
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

def count_lines(path: str) -> int:
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return sum(1 for _ in f)
    except Exception as e:
        print(f"{RED}Wordlist could not be read: {e}{RESET}")
        return -1

def banner():
    print(ASCII)
    print(TITLE)
    print(f"{YELLOW}PurpleRose / PacketBloom identity — colored output & progress bars{RESET}\n")

def menu():
    print(f"{BOLD}{BLUE}Supported Formats:{RESET}")
    for k, name in FORMATS.items():
        print(f"  {CYAN}{k}{RESET}. {name.upper()}")
    choice = input(f"\n{BOLD}{MAGENTA}Select option (1-7): {RESET}").strip()
    return FORMATS.get(choice)

def ask_paths():
    archive = input(f"{BOLD}Archive file path: {RESET}").strip()
    wordlist = input(f"{BOLD}Wordlist file path: {RESET}").strip()
    if not os.path.isfile(archive):
        print(f"{RED}Archive file not found.{RESET}")
        return None, None
    if not os.path.isfile(wordlist):
        print(f"{RED}Wordlist file not found.{RESET}")
        return None, None
    return archive, wordlist

def resolve_binary(is_rust: bool) -> str:
    bin_name = "crack_rs" if is_rust else "crack_go"
    path = shutil.which(bin_name) or (os.path.join(os.getcwd(), bin_name))
    if not os.path.isfile(path) and shutil.which(bin_name) is None:
        print(f"{RED}Executable not found: {bin_name}{RESET}")
        return None
    return path

def run_module(bin_path: str, fmt: str, archive: str, wordlist: str, total: int):
    cmd = [bin_path, "--format", fmt, "--archive", archive, "--wordlist", wordlist, "--total", str(total)]
    print(f"{YELLOW}Running: {RESET}{' '.join(cmd)}\n")
    log_file = os.path.join(LOG_DIR, f"locksmith_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    with open(log_file, "a", encoding="utf-8") as lf:
        lf.write(f"# LockSmith run — {datetime.now().isoformat()}\n")
        lf.write(f"binary={bin_path}\nformat={fmt}\narchive={archive}\nwordlist={wordlist}\ntotal={total}\n\n")

        try:
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
            for line in proc.stdout:
                line = line.rstrip("\n")
                print(line)
                lf.write(line + "\n")
            ret = proc.wait()
            if ret == 0:
                print(f"\n{GREEN}{BOLD}[+] Completed successfully (exit=0).{RESET}")
            else:
                print(f"\n{RED}{BOLD}[-] Module returned error code: {ret}{RESET}")
        except KeyboardInterrupt:
            print(f"\n{RED}Interrupted by user.{RESET}")
        except Exception as e:
            print(f"\n{RED}Execution error: {e}{RESET}")

def main():
    banner()
    fmt = menu()
    if not fmt:
        print(f"{RED}Invalid choice.{RESET}")
        sys.exit(1)

    archive, wordlist = ask_paths()
    if not archive or not wordlist:
        sys.exit(1)

    total = count_lines(wordlist)
    if total <= 0:
        sys.exit(1)

    is_rust = total >= WORDLIST_THRESHOLD
    lang = "Rust" if is_rust else "Go"
    print(f"{BOLD}{BLUE}Wordlist lines: {total} → {lang} module selected.{RESET}")

    bin_path = resolve_binary(is_rust)
    if not bin_path:
        sys.exit(1)

    print(f"{MAGENTA}Legal use only — for your own files.{RESET}\n")
    run_module(bin_path, fmt, archive, wordlist, total)

if __name__ == "__main__":
    main()
