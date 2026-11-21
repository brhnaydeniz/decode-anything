# decode-anything

You throw a string at it, it tells you what it is. If it's an encoding it decodes it; if it's a hash it tries to crack it.

I wrote this because I got tired of staring at a string during OSINT/CTF work wondering "is this hex, base64, or md5?". Single file, no dependencies, just needs Python 3.

*(Türkçe açıklama aşağıda.)*

## What it handles

Encodings (offline, exact): **Hex, URL, Base64, Base32, Binary, Decimal ASCII**

Hashes (with a wordlist): **MD5, SHA-1, SHA-256**

When you pass a hash it finds `rockyou.txt` on its own and unzips it if needed.

## Usage

```bash
git clone https://github.com/brhnaydeniz/decode-anything.git
cd decode-anything

python3 decoder.py "SGVsbG8gV29ybGQ="                   # base64 -> Hello World
python3 decoder.py "48656c6c6f"                         # hex -> Hello
python3 decoder.py "5f4dcc3b5aa765d61d8327deb882cf99"   # md5 -> password
python3 decoder.py "<hash>" --wordlist /path/to/list.txt
```

## rockyou

Cracking hashes needs a wordlist. The tool looks in:

- `/usr/share/wordlists/rockyou.txt` (ships with Kali)
- `/usr/share/wordlists/rockyou.txt.gz` (if zipped, it extracts to `~/.cache/decoder/`, no sudo)
- `rockyou.txt` in the current folder

If none is found it falls back to a small common-password list.

## How it works

Encodings are reversible: the tool checks the character set and length, tries to decode, and reports the type if the result is readable text.

Hashes are not reversible. "Cracking" means hashing every word in a list and comparing it to your target. Online crackers do the same thing with much bigger lists.

## Roadmap

- SQLite-backed cache (for many lookups)
- ROT13, Base58, Morse support
- Multi-layer encodings (e.g. hex inside base64)

## Disclaimer

For education, CTFs, and testing only on systems you're authorized to test. Accessing others' data without permission is a crime.

## License

MIT

---

# decode-anything (Türkçe)

Bir metin atıyorsun, ne olduğunu söylüyor. Kodlamaysa çözüyor, hash'se kırmaya çalışıyor.

OSINT ve CTF'lerde bir dizi görünce "bu hex mi, base64 mü, md5 mi?" diye uğraşmaktan sıkıldığım için yazdım. Tek dosya, hiçbir ek kütüphane yok, Python 3 yetiyor.

## Ne çözüyor

Kodlamalar (internetsiz, kesin): **Hex, URL, Base64, Base32, Binary, Decimal ASCII**

Hash'ler (wordlist ile): **MD5, SHA-1, SHA-256**

Hash girince `rockyou.txt`'yi kendi buluyor, zipliyse kendi açıyor.

## Kullanım

```bash
git clone https://github.com/brhnaydeniz/decode-anything.git
cd decode-anything

python3 decoder.py "SGVsbG8gV29ybGQ="                   # base64 -> Hello World
python3 decoder.py "48656c6c6f"                         # hex -> Hello
python3 decoder.py "5f4dcc3b5aa765d61d8327deb882cf99"   # md5 -> password
python3 decoder.py "<hash>" --wordlist /yol/liste.txt
```

## rockyou

Hash kırmak için kelime listesi lazım. Araç şu yerlere bakıyor:

- `/usr/share/wordlists/rockyou.txt` (Kali'de hazır)
- `/usr/share/wordlists/rockyou.txt.gz` (zipliyse `~/.cache/decoder/` altına açıyor, sudo istemiyor)
- Çalıştığın klasördeki `rockyou.txt`

Hiçbiri yoksa küçük bir yaygın-parola listesiyle devam ediyor.

## Nasıl çalışıyor

Kodlamalar geri çevrilebilir: araç karakter kümesine ve uzunluğa bakıp çözmeyi deniyor, sonuç okunabilir metin çıkarsa o türü yazıyor.

Hash'ler geri çevrilemez. "Kırmak" dediğimiz şey, listedeki her kelimenin hash'ini hesaplayıp aradığın hash'le karşılaştırmak. Online siteler de aynı şeyi çok daha büyük listelerle yapıyor.

## Uyarı

Eğitim, CTF ve sadece yetkili olduğun sistemlerdeki testler için. Başkasının verisine izinsiz erişim suçtur.
