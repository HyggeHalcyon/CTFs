#!/bin/bash


gdb-pwndbg -q -ex 'break *main+44' -ex 'run' -ex 'jump print_flag' -ex 'quit' ./fermat