#!/usr/bin/env python3
import angr
import claripy
import sys
from IPython import embed

def main(exe):
    proj = angr.Project(exe)
    initial_state = proj.factory.entry_state(adrr=0x8048618)

    # manipulating memory
    var1 = claripy.BVS('var1', 8*8)
    var2 = claripy.BVS('var2', 8*8)
    var3 = claripy.BVS('var3', 8*8)
    var4 = claripy.BVS('var4', 8*8)
    initial_state.memory.store(0xab232c0, var1)
    initial_state.memory.store(0xab232c8, var2)
    initial_state.memory.store(0xab232d0, var3)
    initial_state.memory.store(0xab232d8, var4)

    simulation = proj.factory.simgr(initial_state)
    
    simulation.explore(find=0x8048681, avoid=0x804866f)
    return simulation
    
if __name__ == '__main__':
    exe = './symbolic_memory'
    simulation = main(exe)

    if simulation.found:
        print(simulation.found[0].posix.dumps(0))
    else:
        raise Exception('Solution not found')    
    
    # OJQVXIVX LLEAOODW UVCWUVVC AJXJMVKA