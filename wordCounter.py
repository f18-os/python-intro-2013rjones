import re
import sys

def printAll(wordDict,outFile):
    outFile = open(outFile, "w+") # output file restarting if the file exists
    for word in sorted(wordDict): #pulls them out alphabetically sorted. 
        print word + " " + str(wordDict[word])

def processFileLines(fileName):
    lines = [line.rstrip('\n') for line in open(fileName)]
    #define my dictionary 
    wordCounts = {}
    for curLine in lines:
        words = curLine.split()
        for word in words: 
            cleanWord = re.sub(r'[^\w]', ' ', word) #remove all things that are not alphanumeric out of the word then store in dictionary
            if cleanWord in wordCounts.keys():
                    wordCounts[cleanWord] = wordCounts[cleanWord] + 1 
            else:
                    wordCounts[cleanWord] = 1
   
    return wordCounts

def processInputArguments(args):
    #making a strong assumption that we are always given a input followed by the output 
    if len(args) < 3: 
        print("Not enough arguments to run, should contain an input file name and an output file name.")
    else:      
        return "true" 


if processInputArguments(sys.argv) == "true":
    inputFile = sys.argv[1] 
    outptFile = sys.argv[2]
    printAll(processFileLines(inputFile), outptFile)

print("End Program")

   
