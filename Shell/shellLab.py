import os
# THIS WILL ONLY WORK FOR ONE PIPE CMD at a time. 

curToSend = 0; 
cont = True
inputFile = " "; 
outputFile = " "; 
primeCmd = " "; 
curDir = os.environ['PATH']
while (cont):
   print(curDir)
   commandFull = raw_input("$")
   print(commandFull)
   if((commandFull.upper().strip() == "EXIT") or (commandFull.upper().strip() == "$EXIT") ):  #this is my exit conditional
       cont = False
   else:  #if not exit then lets determine our commands.
       print("This is what it reads:" + commandFull)
       allCmdsString = ""
       cmds = commandFull.split() #separate by spaces all commands given. 
       firstCmd = True #determines first command. 
       redirIn = False
       redirOut = False
       piping = False
       pipeToCmds = []
       numPipes = 0 
       firstHalfstr = ""
       secondHalfStr = ""
       firstHalf = True 
       secondHalf = False
       for cmd in cmds: # go through each thing given and determine what to do with it. 
           #need to add code to catch path changes and ps1 modifications. 
           allCmdsString = allCmdsString + " " + cmd # for use if we are missing piping or redirection. 
           if(firstCmd): 
               primeCmd = cmd
               firstCmd = False
           if(redirOut):
               redirOut = False 
               outputFile = cmd             
           if(cmd == ">"):
               redirOut = True
           if(redirIn):
               redirIn = False 
               inputFile = cmd   
           if(cmd == "<"):
               redirIn = True
           if(cmd == "|"): # then we need to pipe the output of the cmds so far into the stuff on the right.  
               piping = True
               if(secondHalf): #then we have both 
                   os.system("python3 piping.py " + " -fh " + firstHalf + " -sh " + secondHalf + " -E ") 

               else: #start storing secondary commands. 
                  secondHalf = True 
                  firstHalf = False 
           if(firstHalf):
                firstHalfstr = firstHalfStr + " " + cmd
           if(secondHalf): 
                secondHalfstr = secondHalfStr + " " + cmd  
       #end of commands.         
       proceed = True
       #should have all my information for a redirect by this point. 
       #now we should call the function passing arguments. 
       if((redirIn == "true") or (redirOut == "true")):
          os.system("python3 p4-redirect.py -c " + primeCmd + " -i " + inputFile + " -o " + outputFile + " -E ")  
          proceed = False
       if(proceed): #then that means there were no major changes to be made. 
           #if((allCmdsString.strip() == "cd")): 
               
           os.system("python3 p3-exec.py " + allCmdsString)  
           
        #okay now we need to reset to allow multiple runs.
                  
                
print "Exited"