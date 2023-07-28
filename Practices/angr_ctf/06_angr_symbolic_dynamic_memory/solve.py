#!/usr/bin/env python3
# https://www.youtube.com/watch?v=QkVzjn3z0iw

import angr
import claripy
import sys
from IPython import embed

def main(exe):
    proj = angr.Project(exe)
    initial_state = proj.factory.entry_state(adrr=0x080486af)

    # creating bitvectors
    buffer0 =  claripy.BVS('buffer0', 8*8)
    buffer1 =  claripy.BVS('buffer1', 8*8)

    # manipulating memory
    # replacing malloc calls pointer
    # to a memory pointer we control
    initial_state.memory.store(0x0a2def74, 0x0804a041, endianness=proj.arch.memory_endness, size=4)
    initial_state.memory.store(0x0a2def7c, 0x0804a041+(8+8), endianness=proj.arch.memory_endness, size=4)
    
    # store the input value on the fake malloc address
    # which is located on the bss section
    initial_state.memory.store(0x0804a041, buffer0, endianness=proj.arch.memory_endness, size=4)
    initial_state.memory.store(0x0804a041+(8+8), buffer1, endianness=proj.arch.memory_endness, size=4)

    simulation = proj.factory.simgr(initial_state)
    simulation.explore(find=0x8048772, avoid=0x8048760)
    return simulation
    
if __name__ == '__main__':
    exe = './symbolic_dynamic_memory'
    simulation = main(exe)

    if simulation.found:
        print(simulation.found[0].posix.dumps(0))
    else:
        raise Exception('Solution not found')    
    
    # OFIJHOXV FBQISOZO