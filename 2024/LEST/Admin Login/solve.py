enc_pass = 'wfpyDnXOIs:qr{hg<Rx||txmj;|oY8'
flag = 'LEST2024{r3vers1ng_a_d0tn3t_pr0grr4mm_s00_e4sily_REPLACE-WITH-PASSWORD_5fea634fb8}'
pt_pass = ''

for idx, c in enumerate(enc_pass):
    if idx % 2 == 0:
        pt_pass += chr(ord(c) - 3)
    else:
        pt_pass += chr(ord(c) - 5)

print("[+] Decrypted Password: ", pt_pass)
print(flag.replace('REPLACE-WITH-PASSWORD', pt_pass))