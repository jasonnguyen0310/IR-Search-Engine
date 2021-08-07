# IR-Search-Engine
Search Engine built in [Python](https://devguide.python.org/documenting/)

# Inspiration
Have you ever wondered how companies like Google, Bing, Baidu, and Yahoo build search engines that know exactly what you are looking for on the web? In my second year of university, I was curious as to what techniques, methods, and framework was used to build high quality search engines. By building this search engine, I hoped to learn and refine my knowledge of information retrieval and computer science in order to someday work for these companies or even start my own entrepreneurial journey!

# Building a Search Engine from Scratch
This information retrieval search engine was built from scratch. This README will address the thought proceses, methods, functions, concepts, and algorithms that are used to create a fully functional search engine!

# Text Processing
When building a **informational retrieval system**, we must have the tools capable of parsing text, processing texting, and storing text from webpages that aid in accurately returning to a query. These tools include processing words, storing words, finding matching words between two files, etc.

Method/Function: **List<Token> tokenize(TextFilePath)**
A method/function that reads in a text file and returns a list of the tokens in that file. For the purposes of this project, a token is a sequence of alphanumeric characters, independent of capitalization (so Apple, apple are the same token).

Method:        **Map<Token,Count> computeWordFrequencies(List<Token>)**
A method/function that counts the number of occurrences of each token in the token list.

Method:         **void print(Frequencies<Token, Count>)**
A method that prints out the word frequency counts

# Web Crawler/Scraper

Starting at a seed page and crawling all links on that page and the page after that. This builds our corpus.
While crawling there are a couple details we want to pay attention to:
  1. Crawl all pages with high textual information content
  2. Detect and avoid infinite traps
  3. Detect and avoid sets of similar pages with no information
  4. Detect and avoid dead URLs that return a 200 status but no data
  5. Detect and avoid crawling very large files, especially if they have low information value
  
# Algorithms
