#! /usr/bin/env python3

import os, subprocess 
# THIS WILL ONLY WORK FOR ONE PIPE CMD at a time. 

curToSend = 0; 
cont = True
inputFile = " "; 
outputFile = " "; 
primeCmd = " "; 
curDir = os.path.dirname(os.path.realpath(__file__))
origDir = curDir
cmdDir= curDir
os.environ['PS1'] = curDir + "$"  #PS1 was not defined thus pulled path and appended $

while (cont): #loop until user puts exit. 
   #print(curDir)

   commandFull = raw_input(os.environ['PS1'])
   #print(commandFull)
   if((commandFull.upper().strip() == "EXIT") or (commandFull.upper().strip() == "$EXIT") ):  #this is my exit conditional
       cont = False
   else:  #if not exit then lets determine our commands.
       #print("This is what it reads:" + commandFull)
       allCmdsString = ""
       cmds = commandFull.split() #separate by spaces all commands given. 
       firstCmd = True #determines first command. 
       redirIn = False
       redirOut = False
       totCmd = 0 
       piping = False
       pipeToCmds = []
       numPipes = 0 
       firstHalfstr = ""
       secondHalfstr = ""
       firstHalf = True 
       redirect = False
       secondHalf = False
       piped = False
       cmdCnt = 0
       setting = False
       setStart = False
       setCont = False
       noSetVar = True
       proceed = True
       contThru = True
       name = ""
       if(commandFull.strip() == ""):
            proceed = False 
       for cmd in cmds: #for all environment variables. 
           
           if(setCont): 
               os.environ[name] = cmd.strip() 
               noSetVar = False
               proceed = False 
               contThru = False
               break
           if((cmd[0:1] == "$") and (cmdCnt == 0)): 
               #then lets assume we are probably setting it to something 
               name = cmd[1:].strip()
               setStart = True 
           if((cmd == "=") and (setStart)):
               setCont = True 
           cmdCnt = 1         
       cmdCnt = 0 
       if(contThru):
            for cmd in cmds: #for specific environment variables. 
                
                if(setCont): 
                    os.environ["PS1"] = cmd.strip()
                    noSetVar = False
                    proceed = False 
                    break
                if((cmd == "$PS1") and (cmdCnt == 0)): 
                    #then lets assume we are probably setting it to something 
                    setStart = True 
                if((cmd == "=") and (setStart)):
                    setCont = True 
                cmdCnt = 1    
       if(noSetVar):
            totCmd = 0; 
            for cmd in cmds: # go through each thing given and determine what to do with it. 
                totCmd = totCmd + 1
                #need to add code to catch path changes and ps1 modifications. 
                # for use if we are missing piping or redirection. 
                notValName = True
                if "$" in cmd.strip():
                    try:
                        cmd =  os.environ[cmd[1:].strip()] #cuts out $
                        notValName = False
                    except: 
                        print("Environment Variable does not exist")
                        proceed = False
                        break; 
                    
                # for use if we are missing piping or redirection. 
                allCmdsString = allCmdsString + " " + cmd     
                if(firstCmd): 
                    primeCmd = cmd
                    firstCmd = False
                if(redirOut):
                    redirOut = False
                    redirect = True
                    outputFile = cmd             
                if(cmd == ">"):
                    redirOut = True
                if(redirIn):
                    redirIn = False
                    redirect = True
                    inputFile = cmd   
                if(cmd == "<"):
                    redirIn = True
                if(cmd == "|"): # then we need to pipe the output of the cmds so far into the stuff on the right.  
                    piping = True
                    secondHalf = True 
                    firstHalf = False 
                if(firstHalf):
                    if(cmd != "|"):
                        firstHalfstr += " " + cmd
                if(secondHalf): 
                    if(cmd != "|"):
                        secondHalfstr += " " + cmd  
                #end of commands.     
            if(secondHalf): #then we have both 
                os.system("python3 piping.py " + " -fh " + firstHalfstr + " -sh " + secondHalfstr + " -E ") 
                piped = True
                proceed = False
            
       #should have all mynformation for a redirect by this point. 
       #now we should call the function passing arguments. 
       if(redirect):
          os.chdir(cmdDir)
          os.system("python3 p4-redirect.py -c " + primeCmd + " -i " + inputFile + " -o " + outputFile + " -cmdp " + cmdDir + " -cuP " + curDir +  " -E " )
          os.chdir(curDir)
          proceed = False
       if(proceed): #then that means there were no major changes to be made. 
           execute = True
           if((allCmdsString.strip() == "cd..")): # then we are changing our directory  backwards one. 
               execute = False
               try: 
                   #print("Start: " + curDir)
                   allDirect = curDir.split("/")
                   #print("before rem: "+allDirect[-1])
                   find = True
                   cnt = -1 
                   while(find):
                       if(allDirect[cnt] != ""):
                           find = False
                       else:
                           cnt = cnt - 1
                           
                   allDirect[cnt] = "" #blank last directory position
                   
                   #print("after rem: "+allDirect[-1])
                   combineNewDirect= ""
                   curCnt = 0 
                   for each in allDirect:
                        if(curCnt != 0):
                            if(each != ""):
                               combineNewDirect += "/" + each
                        else:
                            combineNewDirect +=  each
                            curCnt = 1 
                   #print("end:" +combineNewDirect)     
                   os.chdir(combineNewDirect)
                   curDir = combineNewDirect
                   origDir = curDir
               except: 
                   print("Unable to change directory")
                   os.chdir(origDir)
           allSplit = allCmdsString.split()         
           if((allSplit[0] == "cd")): # then we are changing our directory to whatever follows. 
               execute = False
               curDir += "/" + allSplit[1]
               try: 
                    os.chdir(curDir)
               except: 
                    print("Unable to change directory")
                    os.chdir(origDir)
                    curDir = origDir 
           if((execute) and not (piped)):
               #print("Current: " +curDir)
               os.chdir(cmdDir)
               ec = os.system(" python3 p3-exec.py " + allCmdsString + " -d " + curDir)
               #print("ec: "+ str(ec))
               if(ec != 0): 
                  print("Command Not Found.")
               
               os.chdir(curDir)        
        #okay now we need to reset to allow multiple runs.
                  
                
print "Exited"
