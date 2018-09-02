import re

def printAll(wordDict):
    outFile = open("myWordCntOutput.txt", "w+") # output file restarting if the file exists
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
    
    printAll(wordCounts)

processFileLines("speech.txt")

   
