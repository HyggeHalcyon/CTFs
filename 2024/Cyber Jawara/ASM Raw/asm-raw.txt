00000000000011c9 <check>:
11c9: endbr64
11cd: push   rbp
11ce: mov    rbp,rsp
11d1: sub    rsp,0x20
11d5: mov    QWORD PTR [rbp-0x18],rdi
11d9: mov    rax,QWORD PTR [rbp-0x18]
11dd: mov    rdi,rax
11e0: call   10a0 <strlen@plt>
11e5: mov    DWORD PTR [rbp-0x4],eax
11e8: mov    DWORD PTR [rbp-0x8],0x0
11ef: jmp    1226 <check+0x5d>
11f1: mov    eax,DWORD PTR [rbp-0x8]
11f4: movsxd rdx,eax
11f7: mov    rax,QWORD PTR [rbp-0x18]
11fb: add    rax,rdx
11fe: movzx  edx,BYTE PTR [rax]
1201: mov    eax,DWORD PTR [rbp-0x4]
1204: sub    eax,0x1
1207: sub    eax,DWORD PTR [rbp-0x8]
120a: movsxd rcx,eax
120d: mov    rax,QWORD PTR [rbp-0x18]
1211: add    rax,rcx
1214: movzx  eax,BYTE PTR [rax]
1217: cmp    dl,al
1219: je     1222 <check+0x59>
121b: mov    eax,0x0
1220: jmp    123c <check+0x73>
1222: add    DWORD PTR [rbp-0x8],0x1
1226: mov    eax,DWORD PTR [rbp-0x4]
1229: mov    edx,eax
122b: shr    edx,0x1f
122e: add    eax,edx
1230: sar    eax,1
1232: cmp    DWORD PTR [rbp-0x8],eax
1235: jl     11f1 <check+0x28>
1237: mov    eax,0x1
123c: leave
123d: ret

000000000000123e <main>:
123e: endbr64
1242: push   rbp
1243: mov    rbp,rsp
1246: add    rsp,0xffffffffffffff80
124a: mov    rax,QWORD PTR fs:0x28
1251:
1253: mov    QWORD PTR [rbp-0x8],rax
1257: xor    eax,eax
1259: lea    rax,[rbp-0x70]
125d: mov    rsi,rax
1260: lea    rax,[rip+0xd9d]        # 2004 <_IO_stdin_used+0x4>
1267: mov    rdi,rax
126a: mov    eax,0x0
126f: call   10d0 <__isoc99_scanf@plt>
1274: lea    rax,[rbp-0x70]
1278: mov    rdi,rax
127b: call   10a0 <strlen@plt>
1280: mov    DWORD PTR [rbp-0x74],eax
1283: mov    BYTE PTR [rbp-0x75],0x1
1287: cmp    BYTE PTR [rbp-0x75],0x0
128b: je     12a4 <main+0x66>
128d: lea    rax,[rbp-0x70]
1291: mov    rdi,rax
1294: call   11c9 <check>
1299: test   al,al
129b: je     12a4 <main+0x66>
129d: mov    eax,0x1
12a2: jmp    12a9 <main+0x6b>
12a4: mov    eax,0x0
12a9: mov    BYTE PTR [rbp-0x75],al
12ac: and    BYTE PTR [rbp-0x75],0x1
12b0: cmp    BYTE PTR [rbp-0x75],0x0
12b4: je     12c3 <main+0x85>
12b6: cmp    DWORD PTR [rbp-0x74],0x15
12ba: jne    12c3 <main+0x85>
12bc: mov    eax,0x1
12c1: jmp    12c8 <main+0x8a>
12c3: mov    eax,0x0
12c8: mov    BYTE PTR [rbp-0x75],al
12cb: and    BYTE PTR [rbp-0x75],0x1
12cf: cmp    BYTE PTR [rbp-0x75],0x0
12d3: je     130a <main+0xcc>
12d5: cmp    DWORD PTR [rbp-0x74],0x14
12d9: jle    130a <main+0xcc>
12db: movzx  eax,BYTE PTR [rbp-0x70]
12df: cmp    al,0x61
12e1: jne    130a <main+0xcc>
12e3: movzx  eax,BYTE PTR [rbp-0x6e]
12e7: cmp    al,0x61
12e9: jne    130a <main+0xcc>
12eb: movzx  eax,BYTE PTR [rbp-0x6c]
12ef: cmp    al,0x61
12f1: jne    130a <main+0xcc>
12f3: movzx  eax,BYTE PTR [rbp-0x69]
12f7: cmp    al,0x61
12f9: jne    130a <main+0xcc>
12fb: movzx  eax,BYTE PTR [rbp-0x67]
12ff: cmp    al,0x61
1301: jne    130a <main+0xcc>
1303: mov    eax,0x1
1308: jmp    130f <main+0xd1>
130a: mov    eax,0x0
130f: mov    BYTE PTR [rbp-0x75],al
1312: and    BYTE PTR [rbp-0x75],0x1
1316: cmp    BYTE PTR [rbp-0x75],0x0
131a: je     133e <main+0x100>
131c: cmp    DWORD PTR [rbp-0x74],0x3
1320: jle    133e <main+0x100>
1322: movzx  eax,BYTE PTR [rbp-0x6f]
1326: movsx  edx,al
1329: movzx  eax,BYTE PTR [rbp-0x6d]
132d: movsx  eax,al
1330: sub    eax,0x1
1333: cmp    edx,eax
1335: jne    133e <main+0x100>
1337: mov    eax,0x1
133c: jmp    1343 <main+0x105>
133e: mov    eax,0x0
1343: mov    BYTE PTR [rbp-0x75],al
1346: and    BYTE PTR [rbp-0x75],0x1
134a: cmp    BYTE PTR [rbp-0x75],0x0
134e: je     1365 <main+0x127>
1350: cmp    DWORD PTR [rbp-0x74],0x13
1354: jle    1365 <main+0x127>
1356: movzx  eax,BYTE PTR [rbp-0x5d]
135a: cmp    al,0x6d
135c: jne    1365 <main+0x127>
135e: mov    eax,0x1
1363: jmp    136a <main+0x12c>
1365: mov    eax,0x0
136a: mov    BYTE PTR [rbp-0x75],al
136d: and    BYTE PTR [rbp-0x75],0x1
1371: cmp    BYTE PTR [rbp-0x75],0x0
1375: je     138c <main+0x14e>
1377: cmp    DWORD PTR [rbp-0x74],0xf
137b: jle    138c <main+0x14e>
137d: movzx  eax,BYTE PTR [rbp-0x61]
1381: cmp    al,0x70
1383: jne    138c <main+0x14e>
1385: mov    eax,0x1
138a: jmp    1391 <main+0x153>
138c: mov    eax,0x0
1391: mov    BYTE PTR [rbp-0x75],al
1394: and    BYTE PTR [rbp-0x75],0x1
1398: cmp    BYTE PTR [rbp-0x75],0x0
139c: je     13c0 <main+0x182>
139e: cmp    DWORD PTR [rbp-0x74],0x6
13a2: jle    13c0 <main+0x182>
13a4: movzx  eax,BYTE PTR [rbp-0x6a]
13a8: movsx  edx,al
13ab: movzx  eax,BYTE PTR [rbp-0x6b]
13af: movsx  eax,al
13b2: sub    eax,0x4
13b5: cmp    edx,eax
13b7: jne    13c0 <main+0x182>
13b9: mov    eax,0x1
13be: jmp    13c5 <main+0x187>
13c0: mov    eax,0x0
13c5: mov    BYTE PTR [rbp-0x75],al
13c8: and    BYTE PTR [rbp-0x75],0x1
13cc: cmp    BYTE PTR [rbp-0x75],0x0
13d0: je     13eb <main+0x1ad>
13d2: cmp    DWORD PTR [rbp-0x74],0x11
13d6: jle    13eb <main+0x1ad>
13d8: movzx  edx,BYTE PTR [rbp-0x68]
13dc: movzx  eax,BYTE PTR [rbp-0x5f]
13e0: cmp    dl,al
13e2: jne    13eb <main+0x1ad>
13e4: mov    eax,0x1
13e9: jmp    13f0 <main+0x1b2>
13eb: mov    eax,0x0
13f0: mov    BYTE PTR [rbp-0x75],al
13f3: and    BYTE PTR [rbp-0x75],0x1
13f7: cmp    BYTE PTR [rbp-0x75],0x0
13fb: je     1412 <main+0x1d4>
13fd: cmp    DWORD PTR [rbp-0x74],0xa
1401: jle    1412 <main+0x1d4>
1403: movzx  eax,BYTE PTR [rbp-0x66]
1407: cmp    al,0x63
1409: jne    1412 <main+0x1d4>
140b: mov    eax,0x1
1410: jmp    1417 <main+0x1d9>
1412: mov    eax,0x0
1417: mov    BYTE PTR [rbp-0x75],al
141a: and    BYTE PTR [rbp-0x75],0x1
141e: cmp    BYTE PTR [rbp-0x75],0x0
1422: je     1441 <main+0x203>
1424: lea    rax,[rbp-0x70]
1428: mov    rsi,rax
142b: lea    rax,[rip+0xbd5]        # 2007 <_IO_stdin_used+0x7>
1432: mov    rdi,rax
1435: mov    eax,0x0
143a: call   10c0 <printf@plt>
143f: jmp    1450 <main+0x212>
1441: lea    rax,[rip+0xbc7]        # 200f <_IO_stdin_used+0xf>
1448: mov    rdi,rax
144b: call   1090 <puts@plt>
1450: mov    eax,0x0
1455: mov    rdx,QWORD PTR [rbp-0x8]
1459: sub    rdx,QWORD PTR fs:0x28
1460:
1462: je     1469 <main+0x22b>
1464: call   10b0 <__stack_chk_fail@plt>
1469: leave
146a: ret