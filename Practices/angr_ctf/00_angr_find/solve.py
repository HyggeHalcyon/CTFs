#!/usr/bin/python3
import angr
import claripy
from IPython import embed

def main(exe):
    proj = angr.Project(exe)
    initial_state = proj.factory.entry_state()

    simulation = proj.factory.simgr(initial_state)
    # simulation.explore(find=lambda p: 'Good Job.'.encode('utf8') in p.posix.dumps(1))
    simulation.explore(find=0x804868f, avoid=0x804867d)

    if simulation.found:
        print(simulation.found[0].posix.dumps(0))
    else:
        raise Exception('Solution not found')    

if __name__ == '__main__':
    main('./find')

    # IICLTGRK
