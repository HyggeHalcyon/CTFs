#!/usr/bin/python3
import angr
import claripy
from IPython import embed

def main(exe):
    proj = angr.Project(exe)
    initial_state = proj.factory.entry_state()

    # avoid function that would cause the global
    # variable 'should_succedd' set to 0
    simulation = proj.factory.simgr(initial_state)
    simulation.explore(find=0x80485f7, avoid=0x80485bf)

    if simulation.found:
        print(simulation.found[0].posix.dumps(0))
    else:
        raise Exception('Solution not found')    

if __name__ == '__main__':
    main('./avoid')

    # JLVUSGJZ