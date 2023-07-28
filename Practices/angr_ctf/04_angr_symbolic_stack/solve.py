#!/usr/bin/python3
import angr
import claripy
import sys
from IPython import embed

def main(exe):
    proj = angr.Project(exe)
    initial_state = proj.factory.entry_state(adrr=0x080486ae)
    
    # recreating the stack frame creation such that 
    # our symbols will be placed on the correct place
    # according to the scanf calls:
    # at the beginning of the formation of the stack frame
    # esp is decremented by 28 (adding 28 bytes to the stack)
    # the first variable is loaded 12 bytes relative to ebp
    # the second variable is loading 16 bytes relative to ebp
    # after scanf (which is our entry state), esp is added by 16 
    # reducing the stack by 16, thus esp is located 12 bytes 
    # relative to ebp, which is where our second variable
    # so, we need to add esp by 12 (reducing stack by 12)
    # such that when we push to the stack our first variable 
    # will be aligned how it is supposed to be
    # this is because the next call to complex_function takes one parameter
    # that is supposed to be our first variable
    # read more about how x32 bit functions take parameters
    initial_state.regs.ebp = initial_state.regs.esp
    initial_state.regs.esp += 12
    
    # injecting our symbols according to the place 
    # that the two argument input of scanf
    # 32 for 4 bytes size of int
    unsigned_integer_one =  claripy.BVS('unsigned_integer_one', 32)
    unsigned_integer_two =  claripy.BVS('unsigned_integer_two', 32)
    initial_state.stack_push(unsigned_integer_one)
    initial_state.stack_push(unsigned_integer_two)
    
    # restoring the esp to its previous place
    initial_state.regs.esp -= 12

    simulation = proj.factory.simgr(initial_state)
    simulation.explore(find=0x80486f8, avoid=0x80486e6)
    
    return simulation
    
if __name__ == '__main__':
    exe = './symbolic_stack'
    simulation = main(exe)

    if simulation.found:
        print(simulation.found[0].posix.dumps(0))
    else:
        raise Exception('Solution not found')    
    
    # 2089710965 0012847883
