#! /usr/bin/env python3
#called like so:  os.system("python3 piping.py " + " -fh " + firstHalf + " -sh " + secondHalf + " -E ") 

import os, sys, time, re



r,w = os.pipe()

rc = os.fork()

if rc < 0:
    #os.write(2, ("fork failed, returning %d\n" % rc).encode())
    sys.exit(1)

elif rc == 0:
    os.close(r)
    os.dup2(w, sys.stdout.fileno())
    args = [sys.argv[2], sys.argv[3]]
    
    os.system(sys.argv[2] + " " + sys.argv[3])
    sys.exit(1)     # terminate with error

    
rc2 = os.fork()
if rc2 < 0:
    #os.write(2, ("fork failed, returning %d\n" % rc).encode())
    sys.exit(1)

elif rc2 == 0:
    os.close(w)
    os.close(0) # redirect child's stdin
    os.dup2(r, sys.stdin.fileno())
    os.system(sys.argv[5]) 
    sys.exit(1)     # terminate with error
