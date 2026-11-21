# cozucu.py

Kodlama ve hash çözme/kırma aracı. Bir metnin **hangi kodlama ya da hash** olduğunu otomatik tahmin eder; kodlamaysa çözer, hash'se bir kelime listesiyle kırar.

OSINT ve CTF çalışmalarında, bir dizinin ne olduğunu (hex mi, Base64 mü, MD5 mi) hızlıca anlamak için yazıldı.

## Özellikler

- **Kodlamaları çözer** (internet gerekmez): Hex, URL encoding, Base64, Base32, Binary, Decimal ASCII
- **Hash kırar**: MD5, SHA-1, SHA-256 — bir kelime listesiyle
- **rockyou.txt'yi otomatik bulur**; sıkıştırılmış (`.gz`) ise kendisi açar
- **Kurulum gerektirmez** — sadece Python 3 yeter, hiçbir ek kütüphane yok

## Kurulum

```bash
git clone https://github.com/<kullanici-adin>/cozucu.git
cd cozucu
python3 cozucu.py --help
```

Hepsi bu. Python 3 kurulu her Linux (ve macOS/Windows) makinede çalışır.

## Kullanım

```bash
# Kodlama çözme
python3 cozucu.py "SGVsbG8gV29ybGQ="        # Base64  -> Hello World
python3 cozucu.py "48656c6c6f"              # Hex     -> Hello
python3 cozucu.py "83 116 97 114"           # Decimal -> Star

# Hash kırma (rockyou otomatik bulunur)
python3 cozucu.py "5f4dcc3b5aa765d61d8327deb882cf99"   # MD5 -> password

# Kendi kelime listenle
python3 cozucu.py "<hash>" --wordlist /yol/liste.txt
```

## rockyou.txt

Hash kırmak için bir kelime listesi gerekir. Araç şu konumları otomatik arar:

- `/usr/share/wordlists/rockyou.txt` (Kali Linux'ta hazır gelir)
- `/usr/share/wordlists/rockyou.txt.gz` (sıkıştırılmışsa otomatik açılır)
- Çalıştırıldığı klasördeki `rockyou.txt`

Kali'de liste sıkıştırılmış gelir; araç ilk çalıştırmada onu `~/.cache/cozucu/` altına açar, `sudo` gerektirmez. Kali dışındaki sistemlerde `rockyou.txt`'yi indirip script'in yanına koyman yeterli.

Liste hiç bulunamazsa araç küçük bir yerleşik listeyle (yaygın parolalar) çalışır.

## Nasıl çalışır?

- **Kodlamalar geri çevrilebilir.** Araç her türün parmak izine bakar (karakter kümesi, uzunluk) ve çözüm denemesi okunabilir metin veriyorsa o türü raporlar.
- **Hash'ler geri çevrilemez.** "Kırmak" demek, kelime listesindeki her kelimenin hash'ini hesaplayıp aradığın hash'le karşılaştırmaktır. CrackStation gibi siteler de aynı işi, çok daha büyük listelerle yapar.

## Uyarı

Bu araç eğitim, CTF ve **yalnızca yetkili olduğun** sistemlerdeki güvenlik testleri içindir. Başkalarının hesap ve verilerine izinsiz erişim için kullanmak suçtur.

## Lisans

MIT
