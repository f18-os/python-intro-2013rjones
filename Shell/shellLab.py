import os

curToSend = 0; 
cont = "True"
inputFile = ""; 
outputFile = ""; 
primeCmd = ""; 
while (cont == "True"):
   commandFull = raw_input("Please input a command or type Exit to leave.")
   if((commandFull == "Exit") or (commandFull == "exit")):
       cont = "false"
   else:
       allCmdsString = ""
       cmds = commandFull.split()
       curCnt = 0
       redirIn = "false"
       redirOut = "false"
       for cmd in cmds: 
           allCmdsString = allCmdsString + " " + cmd
           print (cmd) 
           if(curCnt == 0): 
               primeCmd = cmd
               curCnt = curCnt + 1
           if(redirOut == "true"):
               redirOut = "false" 
               outputFile = cmd   
           if(cmd == ">"):
               redirOut = "true"
           if(redirIn == "true"):
               redirIn = "false" 
               inputFile = cmd   
           if(cmd == "<"):
               redirIn = "true"
       #should have all my information for a redirect by this point. 
       #now we should call the function passing arguments. 
       if((redirIn == "true") and (redirOut == "true")):
          os.system("python3 p4-redirect.py " + primeCmd + " " + inputFile + " " + outputFile)  
       #Add in code to handle not both. 
       else: 
          os.system("python3 p3-exec.py " + allCmdsString)  
           

       #Add code to just run executions  
          
       curCnt = 0

                  
                
print "Exited"