## Step 1: cracking PDF user password
```sh
pdfcrack --wordlist=/usr/share/wordlists/rockyou.txt flag_protected.pdf
$password=makanapel
```

## Step 2: Extracting raw stream Javascript code

```sh
pdf-parser --object 10 -w -d dump.js flag_protected.pdf
qpdf --qdf --password=makanapel --object-streams=disable flag_protected.pdf decompressed.pdf
```

References:
- https://www.sentinelone.com/blog/malicious-pdfs-revealing-techniques-behind-attacks/
- https://www.linkedin.com/pulse/analyzing-malicious-pdf-using-pdfid-pdf-parser-tools-mohanraj-a/
- https://stackoverflow.com/questions/11731425/data-extraction-from-filter-flatedecode-pdf-stream-in-php
- https://ourcodeworld.com/articles/read/937/how-to-remove-the-password-of-a-pdf-using-the-qpdf-cli


## Step 3: Deobfuscate Javascript code
1. using https://deobfuscate.io to deobfuscate `decompressed.js` results in `decompressed-deob.js`, stuck here.
2. run `decompressed.js` returns an error shown in `err-msg.js`
3. trying to deobfuscate the error code from `err-msg.js` using https://deobfuscate.io redirects to https://obf-io.deobfuscate.io
4. deobfuscate it, results in `original.js` 