'''
textProcessing.py
Aythor : Jason Nguyen
module contains methods required for text processing
'''

def tokenize(textFilePath):
	# O(n) having n as the size of the file
	tokenList = []
	with open (textFilePath, "r") as myfile:
		for line in myfile:
			line = line.strip()
			line = line.lower()
			tokenList += line.split()
	return tokenList

def computeWordFrequencies(tokenList):
	tokenDict = {}
	for token in tokenList:
		if token in tokenDict:
			tokenDict[token] += 1
		else:
			tokenDict[token] = 1

	return tokenDict

def printWordFrequencies(tokenDict):
	tokenDict = {k: v for k, v in sorted(tokenDict.items(), key = lambda item: item[1])}
	for (key, value) in tokenDict.items():
		print(f"<{key}> = <{value}>")