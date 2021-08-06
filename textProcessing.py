'''
textProcessing.py
Aythor : Jason Nguyen
module contains methods required for text processing
'''

def tokenize(filename):
	# O(n) having n as the size of the file
	tokenList = []
	with open (filename, "r") as myfile:
		for line in myfile:
			line = line.strip()
			line = line.lower()
			tokenList += line.split()
	return tokenList

def computeWordFrequencies(tokenList):
	# O(n) having n as the size of the tokenList
	tokenDict = {}
	for token in tokenList:
		if token in tokenDict:
			tokenDict[token] += 1
		else:
			tokenDict[token] = 1

	return tokenDict

def printWordFrequencies(tokenDict):
	# O(nlogn) having n as the size of the tokenDict
	tokenDict = {k: v for k, v in sorted(tokenDict.items(), key = lambda item: item[1])}
	for (key, value) in tokenDict.items():
		print(f"<{key}> = <{value}>")

def intersection(filename1, filename2):
	# O(n log n)
	numberOfCommonTokens = 0
	tokenList1 = tokenize(filename1)
	tokenList2 = tokenize(filename2)
	tokenDict1 = computeWordFrequencies(tokenList1)
	tokenDict2 = computeWordFrequencies(tokenList2)
	for key in set(tokenDict1.keys()):
		if (key in tokenDict2.keys()):
			numberOfCommonTokens += 1

	return numberOfCommonTokens
