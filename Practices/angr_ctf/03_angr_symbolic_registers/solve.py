#!/usr/bin/python3
import angr
import claripy
import sys
from IPython import embed

# state that being is searched is identified 
# by the address is reached at execution
def main(exe):
    proj = angr.Project(exe)
    initial_state = proj.factory.entry_state(adrr=0x8048869)
    
    # 32 for 32 bit registers
    eax = claripy.BVS('eax', 32)
    ebx = claripy.BVS('ebx', 32)
    edx = claripy.BVS('edx', 32)
    initial_state.regs.eax = eax
    initial_state.regs.ebx = ebx
    initial_state.regs.edx = edx

    simulation = proj.factory.simgr(initial_state)
    simulation.explore(find=0x804892a, avoid=0x804891d)
    
    return simulation

# state that is being searched is indentified
# by the output of stdout by the program execution 
def alternative_solution(exe):
    proj = angr.Project(exe)
    initial_state = proj.factory.entry_state(adrr=0x8048869)
    
    # 32 for 32 bit registers
    eax = claripy.BVS('eax', 32)
    ebx = claripy.BVS('ebx', 32)
    edx = claripy.BVS('edx', 32)
    initial_state.regs.eax = eax
    initial_state.regs.ebx = ebx
    initial_state.regs.edx = edx
    
    def successful(state):
        stdout = state.posix.dumps(sys.stdout.fileno())
        return 'Good Job.'.encode() in stdout
    
    def abort(state):
        stdout = state.posix.dumps(sys.stdout.fileno())
        return 'Try again'.encode() in stdout
    
    simulation = proj.factory.simgr(initial_state)
    simulation.explore(find=successful, avoid=abort)
    return simulation
    
if __name__ == '__main__':
    exe = './symbolic_registers'
    # simulation = main(exe)
    simulation = alternative_solution(exe)

    if simulation.found:
        print(simulation.found[0].posix.dumps(0))
    else:
        raise Exception('Solution not found')    
    
    # e9b37483 7aab5fde 8f5b48ea
