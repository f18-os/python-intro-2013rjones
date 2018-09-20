#! /usr/bin/env python3

import os, sys, time, re

pid = os.getpid()
#os.write(1, ("About to fork (pid:%d)\n" % pid).encode())

rc = os.fork()

if rc < 0:
    #os.write(2, ("fork failed, returning %d\n" % rc).encode())
    sys.exit(1)

elif rc == 0:                   # child
    #os.write(1, ("Child: My pid==%d.  Parent's pid=%d\n" % (os.getpid(), pid)).encode())
    cnt = 0
    saveNxt = False
    for each in sys.argv:
       if(saveNxt):
          os.chdir(each)
          print("dir:" + each)
          saveNxt = False
       if(each.strip() != "-d"):
          cnt += 1 
       else:
          saveNxt = True 
          
 
    args = sys.argv[1:(cnt-1)]
    #print(args)
    for dir in re.split(":", os.environ['PATH']): # try each directory in the path
        program = "%s/%s" % (dir, args[0])
        #os.write(1, ("Child:  ...trying to exec %s\n" % program).encode())
        try:
            os.execve(program, args, os.environ) # try to exec program
        except FileNotFoundError:             # ...expected
            pass                              # ...fail quietly

    #os.write(2, ("Child:    Could not exec %s\n" % args[0]).encode())
    sys.exit(1)                 # terminate with error

else:                           # parent (forked ok)
    #os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" %(pid, rc)).encode())
    childPidCode = os.wait()
    val=childPidCode[1]
    if(val != 0):
        sys.exit(1)
    else:    
        sys.exit(0)
    #os.write(1, ("Parent: Child %d terminated with exit code %d\n" % childPidCode).encode())
