#! /usr/bin/env python3

import os, sys, time, re

pid = os.getpid() # get and remember pid

Pipefds = pipe() #returns two new file descriptors. 
os.set_inheritable(Pipefds[0], True)
os.set_inheritable(Pipefds[1], True)
#os.write(1, ("About to fork (pid=%d)\n" % pid).encode())
#now close fd 1 
normOut = sys.stdout
normIn = sys.stdin

#split passed commands here
# NEED TO ADD 
#ADD REDIRECT CALL IF NECESSARY 

#first child
rc = os.fork()

if rc < 0:
    #os.write(2, ("fork failed, returning %d\n" % rc).encode())
    sys.exit(1)

elif rc == 0:                   # child
    #os.write(1, ("Child: My pid==%d.  Parent's pid=%d\n" % (os.getpid(), pid)).encode())
    os.close(1)
    dup(Pipefds[1]) #changed the output to our pipe.

    fd1 = sys.stdin.fileno() # os.open("p4-output.txt", os.O_CREAT)
    os.set_inheritable(fd1, True)

    for dir in re.split(":", os.environ['PATH']): # try each directory in path
        program = "%s/%s" % (dir, args[0])
        try:
            os.execve(program, args, os.environ) # try to exec program
        except FileNotFoundError:             # ...expected
            pass                              # ...fail quietly 

    os.write(2, ("Child:    Error: Could not exec %s\n" % args[0]).encode())
    sys.exit(1)                 # terminate with error


#SECOND CHILD FOR THE OUTPUT

rc = os.fork()

if rc < 0:
    #os.write(2, ("fork failed, returning %d\n" % rc).encode())
    sys.exit(1)

elif rc == 0:                   # child
    #os.write(1, ("Child: My pid==%d.  Parent's pid=%d\n" % (os.getpid(), pid)).encode())
    os.close(0)
    dup(Pipefds[0]) #changed the output to our pipe.
    
    for dir in re.split(":", os.environ['PATH']): # try each directory in path
        program = "%s/%s" % (dir, args[0])
        try:
            os.execve(program, args, os.environ) # try to exec program
        except FileNotFoundError:             # ...expected
            pass                              # ...fail quietly 

    os.write(2, ("Child:    Error: Could not exec %s\n" % args[0]).encode())
    sys.exit(1)                 # terminate with error

else:                           # parent (forked ok)
    #os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" %(pid, rc)).encode())
    childPidCode = os.wait()
    #os.write(1, ("Parent: Child %d terminated with exit code %d\n" %childPidCode).encode())
    
os.close(3)
os.close(4)
sys.stdin = normIn
sys.stdout = normOut