0xffffffffc0000010 t module_ioctl [chall]

[KALLOC]
alloc break* 0xffffffffc000007f
copy_from_user break* 0xffffffffc0000097
free break* 0xffffffffc00000af

[KFREE]
free break* 0xffffffffc000005d

[VARS]
flag mem 0xffffffffc00021c0
global chunk mem 0xffffffffc0002688

[REFERENCES]
POLL_LIST: https://syst3mfailure.io/corjail/#hl-5-12
SHM_FILE_DATA: https://blog.smallkirby.com/posts/fire-of-salvation/#full-exploit