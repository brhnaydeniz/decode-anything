#!/usr/bin/env python3
# decoder.py
# Takes a string and tries to figure out what it is:
#   - if it's an encoding (hex, base64, url, base32, binary, decimal) -> decode it
#   - if it's a hash (md5, sha1, sha256) -> try to crack it with a wordlist
# Finds rockyou.txt on its own and unzips it if needed. No dependencies.
#
# examples:
#   python3 decoder.py "5f4dcc3b5aa765d61d8327deb882cf99"
#   python3 decoder.py "<value>" --wordlist /path/to/list.txt

import sys
import re
import gzip
import shutil
import base64
import binascii
import hashlib
from pathlib import Path

# common locations where rockyou might live
ROCKYOU_PATHS = [
    "/usr/share/wordlists/rockyou.txt",
    "/usr/share/wordlists/rockyou.txt.gz",
    "/usr/share/seclists/Passwords/Leaked-Databases/rockyou.txt",
    "/opt/wordlists/rockyou.txt",
    str(Path.home() / "rockyou.txt"),
    "rockyou.txt",
    str(Path(__file__).parent / "rockyou.txt"),
]

# we extract a zipped rockyou here (home dir, no sudo needed)
CACHE = Path.home() / ".cache" / "decoder"

# fallback list for when rockyou isn't around
DEFAULT_LIST = [
    "admin", "password", "123456", "12345678", "hello", "root", "toor",
    "qwerty", "letmein", "welcome", "monkey", "dragon", "test", "guest",
    "burhan", "ziraat", "konya", "turkey", "12345", "111111", "iloveyou",
]


def find_rockyou():
    # plain txt first
    for path in ROCKYOU_PATHS:
        p = Path(path)
        if p.is_file() and p.suffix != ".gz":
            return str(p)
    # otherwise extract the zipped one
    for path in ROCKYOU_PATHS:
        p = Path(path)
        if p.is_file() and p.suffix == ".gz":
            return extract_gz(p)
    # last resort: locate
    return try_locate()


def extract_gz(gz):
    CACHE.mkdir(parents=True, exist_ok=True)
    out = CACHE / "rockyou.txt"
    if out.is_file() and out.stat().st_size > 0:
        return str(out)
    print(f"  [*] found zipped list, extracting: {out}")
    with gzip.open(gz, "rb") as src, open(out, "wb") as dst:
        shutil.copyfileobj(src, dst)
    return str(out)


def try_locate():
    try:
        import subprocess
        out = subprocess.run(["locate", "-l", "5", "rockyou.txt"],
                             capture_output=True, text=True, timeout=5).stdout
        for line in out.splitlines():
            p = Path(line.strip())
            if p.is_file() and p.suffix != ".gz":
                return str(p)
    except Exception:
        return None
    return None


def is_readable(data):
    # are the decoded bytes real text, or garbage?
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return False
    good = sum(1 for c in text if 32 <= ord(c) < 127 or c in "\n\t")
    return len(text) > 0 and good / len(text) > 0.85


def crack(h, kind, wordlist):
    h = h.lower()
    func = {"MD5": hashlib.md5, "SHA-1": hashlib.sha1, "SHA-256": hashlib.sha256}[kind]
    if wordlist:
        try:
            with open(wordlist, encoding="utf-8", errors="ignore") as f:
                for line in f:
                    word = line.rstrip("\n")
                    if func(word.encode("utf-8", "ignore")).hexdigest() == h:
                        return word
        except FileNotFoundError:
            pass
    for word in DEFAULT_LIST:
        if func(word.encode()).hexdigest() == h:
            return word
    return None


def decode(s, wordlist):
    results = []
    text = s.strip()
    nospace = text.replace(" ", "")

    # hash? tell by length
    if re.fullmatch(r"[0-9a-fA-F]+", nospace):
        kind = {32: "MD5", 40: "SHA-1", 64: "SHA-256"}.get(len(nospace))
        if kind:
            found = crack(nospace, kind, wordlist)
            if found:
                results.append((kind, f"'{found}'  (found in list)"))
            else:
                results.append((kind, "not in list, need a bigger wordlist"))

    # binary
    if re.fullmatch(r"[01\s]+", text) and len(nospace) % 8 == 0:
        try:
            v = bytes(int(nospace[i:i+8], 2) for i in range(0, len(nospace), 8))
            if is_readable(v):
                results.append(("Binary", v.decode()))
        except ValueError:
            pass

    # space-separated numbers -> ascii
    if re.fullmatch(r"[\d\s]+", text) and " " in text:
        try:
            v = bytes(int(x) for x in text.split())
            if is_readable(v):
                results.append(("Decimal ASCII", v.decode()))
        except (ValueError, OverflowError):
            pass

    # hex
    if re.fullmatch(r"[0-9a-fA-F]+", nospace) and len(nospace) % 2 == 0:
        try:
            v = bytes.fromhex(nospace)
            if is_readable(v):
                results.append(("Hex", v.decode()))
        except ValueError:
            pass

    # url
    if "%" in text:
        from urllib.parse import unquote
        c = unquote(text)
        if c != text:
            results.append(("URL", c))

    # base64
    if re.fullmatch(r"[A-Za-z0-9+/]+={0,2}", text) and len(text) % 4 == 0:
        try:
            v = base64.b64decode(text, validate=True)
            if is_readable(v):
                results.append(("Base64", v.decode()))
        except (binascii.Error, ValueError):
            pass

    # base32
    if re.fullmatch(r"[A-Z2-7]+={0,6}", text) and len(text) % 8 == 0:
        try:
            v = base64.b32decode(text)
            if is_readable(v):
                results.append(("Base32", v.decode()))
        except (binascii.Error, ValueError):
            pass

    return results


def is_hash(s):
    b = s.strip().replace(" ", "")
    return bool(re.fullmatch(r"[0-9a-fA-F]+", b)) and len(b) in (32, 40, 64)


HELP = """decoder.py - encoding and hash decoder

usage:
  python3 decoder.py "<value>"
  python3 decoder.py "<value>" --wordlist /path/to/list.txt

examples:
  python3 decoder.py "5f4dcc3b5aa765d61d8327deb882cf99"   # md5 -> password
  python3 decoder.py "SGVsbG8gV29ybGQ="                   # base64 -> Hello World
  python3 decoder.py "48656c6c6f"                         # hex -> Hello
"""


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(HELP)
        return

    value = args[0]
    wordlist = None
    if "--wordlist" in args:
        i = args.index("--wordlist")
        if i + 1 < len(args):
            wordlist = args[i + 1]

    if is_hash(value) and not wordlist:
        wordlist = find_rockyou()
        if wordlist:
            print(f"  [*] wordlist: {wordlist}")
        else:
            print("  [!] rockyou not found, using small built-in list")

    print(f"\n> {value}")
    print("-" * 50)
    results = decode(value, wordlist)
    if not results:
        print("  couldn't decode, not a recognized type")
    else:
        for kind, out in results:
            print(f"  [{kind}] -> {out}")
    print()


if __name__ == "__main__":
    main()
