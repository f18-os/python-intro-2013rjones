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
       cmds = commandFull.split()
       curCnt = 0
       redirIn = "false"
       redirOut = "false"
       for cmd in cmds: 
           print (cmd) 
           if(curCnt == 0): 
               primeCmd = cmd
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
       executePgm = os.path.dirname(os.path.abspath(__file__)) + "/p4-redirectMod.py"
       os.system("python3 "+executePgm +" " + primeCmd + " " + inputFile + " " + outputFile)  
       curCnt = 0

                  
                
print "Exited"