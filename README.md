# 🔑 LockSmith

<p align="center">
LockSmith is a prototype archive password recovery toolkit.  
It orchestrates Rust and Go backends through a unified Python CLI,  
providing modular design, logging, and distinctive banner-styled output.
</p>

---

##  Features
- **Unified CLI:** Automatically selects backend (Rust for large wordlists, Go for small).  
- **Archive formats:** Supports ZIP, RAR, TAR.GZ, 7Z, BZ2, GZ, LZMA.  
- **Logging:** Timestamped logs stored under `logs/`.  
- **Modular design:** Easily extendable with new backends or formats.  

---

##  Installation
```bash
git clone https://github.com/yourname/LockSmith.git
cd LockSmith

# Build Rust backend
cargo build --release

# Build Go backend
go build crack.go
