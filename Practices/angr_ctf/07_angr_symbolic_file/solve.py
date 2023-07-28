#!/usr/bin/env python3
# https://www.youtube.com/watch?v=QkVzjn3z0iw

import angr
import claripy
import sys
from IPython import embed

def main(exe):
    proj = angr.Project(exe)
    initial_state = proj.factory.entry_state(adrr=0x80488e5)

    # creating bitvectors
    contents =  claripy.BVS('contents', 64*8)
    fd = angr.storage.SimFile("FOQVSBZB.txt", content=contents)

    # manipulating memory
    initial_state.fs.insert("FOQVSBZB.txt" ,fd)

    simulation = proj.factory.simgr(initial_state)
    simulation.explore(find=0x804899e, avoid=0x8048984)
    return simulation
    
if __name__ == '__main__':
    exe = './symbolic_file'
    simulation = main(exe)

    if simulation.found:
        print(simulation.found[0].posix.dumps(0))
    else:
        raise Exception('Solution not found')    
    
    # OBAXRUZT\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00