#! /usr/bin/env python3

import os, subprocess, sys, re

def piping(leftCmd, rightCmd): 
    r,w = os.pipe()

    rc = os.fork()

    if rc < 0:
        #os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)

    elif rc == 0:
        os.close(r)
        os.dup2(w, sys.stdout.fileno())
        os.close(2)
        
        rc3 = os.system(leftCmd)
        if(rc3 != 0): 
            sys.exit(1)
        else:
            sys.exit(0)     # terminate with no error

        
        
    rc2 = os.fork()
    if rc2 < 0:
        #os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)

    elif rc2 == 0:
        os.close(w)
        os.close(2)
        os.close(0) # redirect child's stdin
        os.dup2(r, sys.stdin.fileno())
        try:
            rc4 = os.system(rightCmd)
            if(rc4 != 0):
                    print("Invalid Right Command")
                    sys.exit(1)
            else:
                    sys.exit(0)     # terminate with no error
        except: 
            sys.exit(1)

def forkRedirectOut(fullCommand): 
    
    pid = os.getpid()               # get and remember pid
    splitCommand = fullCommand.split(" ")
    
    rc = os.fork()
    if rc < 0:
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)

    elif rc == 0:                   # child
        if ">" in splitCommand: #change out
            nextElem = False 
            Command = ""  
            for element in splitCommand:
                if(nextElem):
                    os.close(1) # redirect child's stdout
                    sys.stdout = open(element, "w+")
                    os.set_inheritable(1, True)

                if(element != ">" and not nextElem): 
                    Command = Command + element + " "
                else: 
                    nextElem = True

            try:
               os.system(Command) # try to exec program
            except FileNotFoundError:  # ...expected
               pass                              # ...fail quietly 

            sys.exit(1)                 # terminate with error
        else: #change in 
            nextElem = False 
            Command = ""  
            for element in splitCommand:
                if(nextElem):
                    os.close(0)
                    sys.stdin = open(element)
                    fd1 = sys.stdin.fileno() # os.open("p4-output.txt", os.O_CREAT)
                    os.set_inheritable(fd1, True)
                if(element != "<" and not nextElem): 
                    Command = Command + element + " "
                else: 
                    nextElem = True

            try:
               os.system(Command) # try to exec program
            except FileNotFoundError:  # ...expected
               pass                              # ...fail quietly 

            sys.exit(1)                 # terminate with error

    else: #parent (forked ok)
        childPidCode = os.wait()



def forkExec(command): 
    try:
        pid = os.getpid()
        rc = os.fork()
        if rc < 0:
            os.write(2, ("fork failed, returning %d\n" % rc).encode())
            sys.exit(1)
        elif rc == 0:                   # child
            output = subprocess.check_output(['bash','-c', command])
            print(output.decode("utf-8"))
        else:                           # parent (forked ok)
            os.wait()
    except: 
        pass
def changeDir(fullCommand): 
    splitCommand = fullCommand.split(" ")
    try:
        os.chdir(os.getcwd() +"/"+ splitCommand[1] + "/")
    except Exception as ex:
        print("Directory not found")
def stepBackDir(): 
    execute = False
    try: 
        allDirect = curDir.split("/")
        find = True
        cnt = -1 
        while(find):
            if(allDirect[cnt] != ""):
                find = False
            else:
                cnt = cnt - 1
                
        allDirect[cnt] = "" #blank last directory position

        combineNewDirect= ""
        curCnt = 0 
        for each in allDirect:
            if(curCnt != 0):
                if(each != ""):
                    combineNewDirect += "/" + each
            else:
                combineNewDirect +=  each
                curCnt = 1      
        os.chdir(combineNewDirect)
    except: 
        print("Unable to change directory")
        os.chdir(origDir)




if os.path.isfile("KILL.txt"): 
   os.remove("KILL.txt")

cont = True
commandFull =""
curDir =  os.getcwd()
origDir = curDir
setPs1 = True

while (cont): #loop until user puts exit.
   if os.path.isfile(origDir + "/KILL.txt"): 
       sys.exit() 
   #first let us change ps1 to change the prompt. 
   try: 
       cur_dir = os.environ['PS1']
       if(setPS1): 
           cur_dir = os.getcwd() + "$"
   except:     
       os.environ['PS1'] = os.getcwd() + "$"
       cur_dir = os.environ['PS1']
       
       
   commandFull = input(os.environ['PS1'])
   
   if commandFull != "": 
        splitCommand = commandFull.split()
        
        
        if((commandFull.upper().strip() == "EXIT") or (commandFull.upper().strip() == "$EXIT") ):  #this is my exit conditional
            cont = False
        else:
            didSomething = False
            nxtSave = False
            if "$PS1" in splitCommand: 
                if "=" in splitCommand: 
                    for element in splitCommand: 
                         if nxtSave: 
                            os.environ['PS1'] = element
                            setPS1 = False
                         if element == "=": 
                            nxtSave = True
                didSomething = True
            if "cd" in splitCommand: 
                changeDir(commandFull)
                didSomething = True
            if "cd.." in splitCommand: 
                stepBackDir()
                didSomething = True 
            if "<"  in splitCommand: 
                forkRedirectOut(commandFull)
                didSomething = True 
            if ">" in splitCommand: 
                forkRedirectOut(commandFull)
                didSomething = True 
            if "|" in splitCommand:
                 leftCmd = ""
                 rightCmd = ""
                 rightNow = False 
                 for element in splitCommand:
                     if rightNow: 
                         rightCmd = rightCmd + element + " "
                     if element == "|": 
                         rightNow = True 
                     if not rightNow: 
                         leftCmd = leftCmd + element + " " 
                 #we now have the left and right of the pipe. 
                 piping(leftCmd,rightCmd)
            if(not didSomething): 
                forkExec(commandFull)
        
                  
open("KILL.txt", "w+")                
print("Exited")
sys.exit()
