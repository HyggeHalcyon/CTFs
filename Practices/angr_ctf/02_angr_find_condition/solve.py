#!/usr/bin/python3
import angr
import claripy
import sys
from IPython import embed

# state that being is searched is identified 
# by the address is reached at execution
def main(exe):
    proj = angr.Project(exe)
    initial_state = proj.factory.entry_state()

    simulation = proj.factory.simgr(initial_state)
    simulation.explore(find=0x804ba96, avoid=0x804ba81)
    
    return simulation

# state taht is being searched is indentified
# by the output of stdout by the program execution 
def alternative_solution(exe):
    proj = angr.Project(exe)
    initial_state = proj.factory.entry_state()
    
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
    exe = './find_condition'
    simulation = main(exe)
    # simulation = alternative_solution(exe)

    if simulation.found:
        print(simulation.found[0].posix.dumps(0))
    else:
        raise Exception('Solution not found')    
    
    # OHYJUMBE
