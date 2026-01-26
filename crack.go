// crack.go — unified Go module for short wordlists
// Build: go build -o crack_go crack.go
package main

import (
    "bufio"
    "flag"
    "fmt"
    "os"
    "os/exec"
    "strings"

    "github.com/alexmullins/zip"
)

// ANSI colors
const (
    reset  = "\033[0m"
    green  = "\033[32m"
    red    = "\033[31m"
    yellow = "\033[33m"
    cyan   = "\033[36m"
    bold   = "\033[1m"
)

// progress bar helper
func progressBar(done, total int) string {
    width := 30
    if total <= 0 { total = 1 }
    ratio := float64(done) / float64(total)
    fill := int(ratio * float64(width))
    if fill > width { fill = width }
    bar := strings.Repeat("█", fill) + strings.Repeat("▒", width-fill)
    return fmt.Sprintf("%s%s[%s] %d/%d (%.1f%%)%s", cyan, bold, bar, done, total, ratio*100, reset)
}

// format-specific password attempts
func tryZip(archive, password string) bool {
    r, err := zip.OpenReader(archive)
    if err != nil { return false }
    defer r.Close()
    for _, f := range r.File {
        f.SetPassword(password)
        rc, err := f.Open()
        if err != nil { return false }
        rc.Close()
    }
    return true
}

func tryRar(archive, password string) bool {
    cmd := exec.Command("unrar", "t", "-p"+password, "-y", archive)
    return cmd.Run() == nil
}

func try7z(archive, password string) bool {
    cmd := exec.Command("7z", "t", "-p"+password, archive)
    return cmd.Run() == nil
}

func tryPlaceholder(_archive, _password string) bool {
    return false
}

func main() {
    format := flag.String("format", "", "archive format (zip, rar, 7z, targz, bz2, gz, lzma)")
    archive := flag.String("archive", "", "archive file path")
    wordlist := flag.String("wordlist", "", "wordlist file path")
    total := flag.Int("total", 0, "total lines in wordlist")
    flag.Parse()

    if *format == "" || *archive == "" || *wordlist == "" {
        fmt.Println(red + "Missing arguments." + reset)
        os.Exit(2)
    }

    file, err := os.Open(*wordlist)
    if err != nil {
        fmt.Println(red + "Cannot open wordlist: " + err.Error() + reset)
        os.Exit(2)
    }
    defer file.Close()

    sc := bufio.NewScanner(file)
    done := 0
    for sc.Scan() {
        pw := strings.TrimSpace(sc.Text())
        done++
        var ok bool
        switch *format {
        case "zip":
            ok = tryZip(*archive, pw)
        case "rar":
            ok = tryRar(*archive, pw)
        case "7z":
            ok = try7z(*archive, pw)
        case "targz", "bz2", "gz", "lzma":
            ok = tryPlaceholder(*archive, pw)
        default:
            fmt.Println(red + "Unsupported format." + reset)
            os.Exit(2)
        }

        if ok {
            fmt.Printf("\n%s%s[+] Password found:%s %s\n", green, bold, reset, pw)
            os.Exit(0)
        } else {
            fmt.Println(progressBar(done, *total) + "  try: " + pw)
        }
    }
    fmt.Println("\n" + red + "[-] Password not found in wordlist." + reset)
    os.Exit(1)
}
