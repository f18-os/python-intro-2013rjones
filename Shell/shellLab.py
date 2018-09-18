#! /usr/bin/env python3

import os
# THIS WILL ONLY WORK FOR ONE PIPE CMD at a time. 

curToSend = 0; 
cont = True
inputFile = " "; 
outputFile = " "; 
primeCmd = " "; 
curDir = os.path.dirname(os.path.realpath(__file__))
origDir = curDir
cmdDir= curDir
while (cont):
   #print(curDir)
   commandFull = raw_input("$")
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
       piping = False
       pipeToCmds = []
       numPipes = 0 
       firstHalfstr = ""
       secondHalfstr = ""
       firstHalf = True 
       redirect = False
       secondHalf = False
       piped = False
       for cmd in cmds: # go through each thing given and determine what to do with it. 
           #need to add code to catch path changes and ps1 modifications. 
           allCmdsString = allCmdsString + " " + cmd # for use if we are missing piping or redirection. 
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
               if(secondHalf): #then we have both 
                   os.system("python3 piping.py " + " -fh " + firstHalf + " -sh " + secondHalf + " -E ") 
                   piped = True
               else: #start storing secondary commands. 
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
               
       proceed = True
       #should have all my information for a redirect by this point. 
       #now we should call the function passing arguments. 
       if(redirect):
          os.chdir(cmdDir)
          os.system("python3 p4-redirect.py -c " + primeCmd + " -i " + inputFile + " -o " + outputFile + " -cmdp " + cmdDir + " -cuP " + curDir +  " -E " )
          os.chdir(curDir)
          proceed = False
       if(proceed): #then that means there were no major changes to be made. 
           execute = True
           if((allCmdsString.strip() == "cd..")):
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
           if((allSplit[0] == "cd")):
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
               os.system(" python3 p3-exec.py " + allCmdsString + " -d " + curDir)
               os.chdir(curDir)        
        #okay now we need to reset to allow multiple runs.
                  
                
print "Exited"
