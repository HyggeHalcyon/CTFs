#!/usr/bin/env python3
# https://www.youtube.com/watch?v=QkVzjn3z0iw

import angr
import claripy
import sys
from IPython import embed

def main(exe):
    proj = angr.Project(exe)
    initial_state = proj.factory.entry_state(adrr=start)

    # creating bitvectors
    rdi =  claripy.BVS('rdi', 32)
    rdx =  claripy.BVS('rsi', 32)
    
    # manipulating registers
    initial_state.regs.rdi = rdi
    initial_state.regs.rsi = rsi

    # manipulating memory
    initial_state.memory.store(memory, value, endianness=proj.arch.memory_endness, size=8)

    # manipulating stack
    initial_state.stack_push(value)
    initial_state.stack_push(value)

    simulation = proj.factory.simgr(initial_state)
    
    # alternative simulation explore method
    def successful(state):
        stdout = state.posix.dumps(sys.stdout.fileno())
        return 'String if successful'.encode() in stdout
    
    def abort(state):
        stdout = state.posix.dumps(sys.stdout.fileno())
        return 'String if failed'.encode() in stdout
    
    simulation.explore(find=success, avoid=abort)
    return simulation
    
if __name__ == '__main__':
    exe = './'
    simulation = main(exe)

    if simulation.found:
        print(simulation.found[0].posix.dumps(0))
    else:
        raise Exception('Solution not found')    
    
    # 