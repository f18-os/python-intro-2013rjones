#! /usr/bin/env python3
#passes in what kind of args are given. 
#standard arg pass: 
#os.system("python3 p4-redirect.py -c " + primeCmd + " -i " + inputFile + " -o " + outputFile + " -E ")  

import os, sys, time, re

outputFile= ""
inputFile = ""
cmd = ""
curDir = ""
cmdDir = ""
myArgs = ""
normIn = ""
normOut = ""
errOut = ""
prev = ""
for x in sys.argv[1:]:
    if((prev.strip() == "-c") and (x.strip() != "-i")): 
        cmd = x.strip() 
    
    if((prev.strip() == "-i") and (x.strip() != "-o")): 
        inputFile = x.strip() 
        
    if((prev.strip() == "-o") and (x.strip() != "-cmdp")): 
        outputFile = x.strip()
    if((prev.strip() == "-cmdp") and (x.strip() != "-cuP")): 
        cmdDir = x.strip()     
    if((prev.strip() == "-cuP") and (x.strip() != "-E")): 
        curDir = x.strip()     
    
    prev = x  


pid = os.getpid()               # get and remember pid

#os.write(1, ("About to fork (pid=%d)\n" % pid).encode())

rc = os.fork()

if rc < 0:
    #os.write(2, ("fork failed, returning %d\n" % rc).encode())
    sys.exit(1)

elif rc == 0:                   # child
    #os.write(1, ("Child: My pid==%d.  Parent's pid=%d\n" % (os.getpid(), pid)).encode())
    #print(sys.argv)

    os.chdir(curDir)
    args = [sys.argv[2], sys.argv[4]]

    normOut = sys.stdout
    normIn = sys.stdin
    

    if(outputFile != ""):
        
        os.close(1) # redirect child's stdout
        sys.stdout = open(outputFile, "w")
        fd = sys.stdout.fileno() # os.open("p4-output.txt", os.O_CREAT)
        os.set_inheritable(fd, True)
    
    if(inputFile != ""):
        os.close(0)
        sys.stdin = open(inputFile)
        fd1 = sys.stdin.fileno() # os.open("p4-output.txt", os.O_CREAT)
        os.set_inheritable(fd1, True)
    #os.chdir(cmdDir)
    for dir in re.split(":", os.environ['PATH']): # try each directory in path
        program = "%s/%s" % (dir, args[0])
        try:
            os.execve(program, args, os.environ) # try to exec program
        except FileNotFoundError:             # ...expected
            pass                              # ...fail quietly 
    #os.chdir(curDir)
    sys.stdout = normOut 
    sys.stdin = normIn 
    os.write(2, ("Child:    Error: Could not exec %s\n" % args[0]).encode())
    sys.exit(1)                 # terminate with error

else:                           # parent (forked ok)
    #os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" %(pid, rc)).encode())
    childPidCode = os.wait()

    #os.write(1, ("Parent: Child %d terminated with exit code %d\n" %childPidCode).encode())
    
