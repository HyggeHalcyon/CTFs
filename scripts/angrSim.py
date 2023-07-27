#!/usr/bin/env python3
# https://www.youtube.com/watch?v=QkVzjn3z0iw

import angr
import sys
import os
import claripy
from IPython import embed

def main():
  proj = angr.Project(sys.argv[1])
  initial_state = proj.factory.entry_state()

  simgr = proj.factory.simgr(initial_state, veritesting=False)
  simgr.explore(find=lambda p: 'Good Job.'.encode('utf8') in p.posix.dumps(1))
#   simgr.explore(find= , avoid=)

  print(pg)
  print(repr(pg.found[0].posix.dumps(0)))

if __name__ == '__main__':
  main()
  
import angr