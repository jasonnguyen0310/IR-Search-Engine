from textProcessing import tokenize, computeWordFrequencies, printWordFrequencies

'''
main.py
Aythor : Jason Nguyen
module contains search engine code
'''


if __name__ == "__main__":
	tokenList = tokenize("test.txt")
	print(tokenList)
	tokenDict = computeWordFrequencies(tokenList)
	printWordFrequencies(tokenDict)

