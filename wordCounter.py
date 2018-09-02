#Author Ryan Jones 
#Last Modified: 9/1/2018
#Purpose of proogram: Thiss program when given an input file name and an output file name will loop determine the 
#amount of times each distinct word is in the input file and then write to the output file the words in alphabetical order 
# with the number of times it shows up in the file.
#General guidance and direction was found through https://www.tutorialspoint.com/python/python_basic_syntax.htm  
#However all of the coding and problem solving was done entirely by myself with the above site as a syntactical reference. 
import re
import sys

#This method writes to a file 
def printAll(wordDict,outFile):
    sysOutOrig = sys.stdout
    outFile = open(outFile, "w+") # output file restarting if the file exists
    sys.stdout = outFile # will now be able to print to file instead of using write(...) 
    for word in sorted(wordDict): #pulls them out alphabetically sorted. 
        print word + " " + str(wordDict[word])
    sys.stdout = sysOutOrig # reset to original 
    outFile.close()
#This method takes in the input file taking the lines and pulling the words in lowercase counting them into a dictionary     
def processFileLines(fileName):
    lines = [line.rstrip('\n') for line in open(fileName)]
    #define my dictionary 
    wordCounts = {}
    for curLine in lines: #loop through each line individually 
        curLine = re.sub(r'[!.,?:;-]' ,' ', curLine) #takes out any that are in [] and replaces with a space in the line. 
        curLine = re.sub(r"'" ,' ', curLine) #removes apastrophies 
        curLine = re.sub(r'"', " ", curLine) #removes quotations
        words = curLine.split()
        for word in words: 
            cleanWord = word.strip().lower() #remove all spaces and change to lowercase

            if cleanWord in wordCounts.keys(): #either initialize word in dictionary with value 1 or increment up by 1 
                    wordCounts[cleanWord] = wordCounts[cleanWord] + 1 
            else:
                    wordCounts[cleanWord] = 1
   
    return wordCounts
#This method verifies we have the proper amount of arguments 
def processInputArguments(args):
    #making a strong assumption that we are always given a input followed by the output 
    if len(args) < 3: 
        print("Not enough arguments to run, should contain an input file name and an output file name.")
    else:      
        return "true" 
#Main logic portion 
if processInputArguments(sys.argv) == "true":
    inputFile = sys.argv[1] 
    outptFile = sys.argv[2]
    printAll(processFileLines(inputFile), outptFile)
    

   
