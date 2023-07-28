# Practical Platforms 
## ROP Emporium
| Challenge | x86 | x64 | ARMv5 | MIPS |  Description | 
| --- | :---: | :---: | :---: | :---: | --- |
| ret2win | ✅ | ✅ | ❌ | ❌ | Classical ret2win | 
| split | ✅ | ✅ | ❌ | ❌ | ROP with one parameter | 
| callme | ✅ | ✅ | ❌ | ❌ | multiple function and args ROP | 
| write4 | ✅ | ✅ | ❌ | ❌ | write string to memory and utilizing it as args | 
| badchars | ✅ | ✅ | ❌ | ❌ | bypassing blacklisted bytes | 
| fluff | ❌ | ❌ | ❌ | ❌ | Description | 
| pivot | ❌ | ❌ | ❌ | ❌ | Description | 
| ret2csu | ❌ | ❌ | ❌ | ❌ | Description | 

## Angr CTF
| Challenge | Description | 
| --- | --- |
| find | baby angr |
| avoid | avoiding call to a bad function |
| find condition | combining both practice + different success methodology |
| symbolic registers | controlling registers where user input is stored |
| symbolic stack | replicating the stack frame creation and controlling user input in the stack |
| symbolic memory | controlling user input in the global variable |
| symbolic dynamic memory | controlling user input that is being dynamically allocated by malloc |
| symbolic file | dealing with file descriptors where user input is stored and loaded |

based upon this [repo](https://github.com/jakespringer/angr_ctf)

## TryHackMe
| Room | Category | Description | 
| --- | :---: | --- |
| PWN101 | Pwn | basic stack-based challenges  | 