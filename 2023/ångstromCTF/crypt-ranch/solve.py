#!usr/bin/python3

ct = 'rtkw{cf0bj_czbv_nv\'cc_y4mv_kf_kip_re0kyvi_uivjj1ex_5vw89s3r44901831}'
vocab = 'abcdefghijklmnopqrstuvwxyz' 

flag = list(ct)
for i in range(1, 26):
    for j in range(len(ct)):
        if(ct[j] in vocab):
            flag[j] = vocab[ (vocab.index(ct[j]) + i) % len(vocab) ]
    
    decryptedflag = ''.join(flag)
    if('actf{' in decryptedflag):
        print('flag: ', decryptedflag)