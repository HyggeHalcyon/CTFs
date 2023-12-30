# init func  
  
```  
fd = *(home/kali/SharedFolder/hidden/main)  
  
[  
	call open@plt  
	path = fd  
]  
  
[  
	call __xpg_basename@plt  
	path = fd  
	  
	ret = *(main)  
]  
  
[  
	call maps()  
	  
	ret = piebase address of the binary  
]  
  
[  
	call read()@plt  
	fd = fd  
	buf = head@stack  
	nbytes = 64  
	  
	head@stack = 64 bytes of binary header  
]  
  
[  
	call lseek()@plt  
	fd = fd   
	offset = 0x3a78  
	  
	set the pointer to fd at offset 0x3a78  
]  
  
[  
	call read()@plt  
	fd = fd  
	buf = tail@stack  
	nbytes = 64  
	  
	tail@stack = 64 bytes starting at the fd pointer  
	which is the last 64 byte of the binary  
	using `dd skip=14968 count=64 if=main  of=header bs=1`  
	xxd on `header`  
]  
  
[  
	call malloc@plt  
	size: 0x115  
	  
	ret = heap  
]  
  
[  
	call lseek()@plt  
	fd = fd   
	offset = 0x321e  
	  
	set the pointer to fd at offset 0x321e  
]  
  
[  
	call read()@plt  
	fd = fd  
	buf = heap  
	nbytes = 0x115  
	  
	`dd skip=12830 count=277 if=main  of=tail bs=1`  
]  
  
[  
	call lseek()@plt  
	fd = fd   
	offset = 0x3338  
	  
	set the pointer to fd at offset 0x3338  
]  
   
LOOP; searches for the ".encrypted" section in the vtable located at the tail of the binary  
[  
	call read()@plt  
	fd = fd  
	buf = tail@stack  
	nbytes = 64  
	  
	  
]  
  
// SKIPPED  
  
[  
	call mprotect()@plt  
	addr: code section (page2)  
	len: 0x1000  
	prot: 0x7  
	  
	  
]  
```