# what confuses you is the ip and the argv variable
# this highlights it https://0xrick.github.io/pwn/collision/

print(f'first four payloads    = {hex(0x21dd09ec // 5)}')
print(f'last remaining payload = {hex(0x21dd09ec - 0x6c5cec8 * 4)}')

# remote: 
# ./col `python -c 'print "\xc8\xce\xc5\x06"*4 + "\xcc\xce\xc5\x06"'`