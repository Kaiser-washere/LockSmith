<h1 align="center">🔑 LockSmith</h1>

<p align="center">
A prototype archive password recovery toolkit built with Rust, Go, and Python orchestration.  
LockSmith unifies multiple backends under a single CLI with banner-styled output and logging.  
</p>

<hr/>

<pre align="center">
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
⠀⠀⠀⠀⠈⠒⠓⠃⠀
</pre>

<hr/>

<h2>✨ Features</h2>
<ul>
  <li><b>Unified CLI:</b> <code>core.py</code> selects backend automatically (Rust for large wordlists, Go for small).</li>
  <li><b>Archive formats:</b> ZIP, RAR, TAR.GZ, 7Z, BZ2, GZ, LZMA.</li>
  <li><b>Logging:</b> Each run saved under <code>logs/</code> with timestamped files.</li>
  <li><b>Colored output:</b> ANSI colors + ASCII banner for distinctive CLI identity.</li>
  <li><b>Modular design:</b> Extendable with new backends or formats.</li>
</ul>

<hr/>

<h2>📦 Installation</h2>

```bash
git clone https://github.com/yourname/LockSmith.git
cd LockSmith

# Build Rust backend
cargo build --release

# Build Go backend
go build crack.go
```
<hr/>

<h2>🚀 Usage</h2>

```
python core.py
```
<p>
The CLI will:
</p>
<ol>
<li>Show banner and supported formats.</li>
<li>Ask for archive path and wordlist path.</li>
<li>Count wordlist lines → decide Rust or Go backend.</li>
<li>Run the selected binary with parameters.</li>
<li>Log output to <code>logs/</code>.</li>
</ol>

<hr/>

<h2>⚙️ Requirements</h2>
<ul>
<li>Python 3.10+</li>
<li>Rust 1.70+</li>
<li>Go 1.20+</li>
</ul>

<hr/>

<h2>📜 License</h2>
<p>
MIT release — for educational and research purposes only.
Do not use for unauthorized access or illegal activities.
</p>
