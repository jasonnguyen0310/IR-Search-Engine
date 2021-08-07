# IR-Search-Engine
Search Engine built in [Python](https://devguide.python.org/documenting/)

# Inspiration
Have you ever wondered how companies like Google, Bing, Baidu, and Yahoo build search engines that know exactly what you are looking for on the web? In my second year of university, I was curious as to what techniques, methods, and framework was used to build high quality search engines. By building this search engine, I hoped to learn and refine my knowledge of information retrieval and computer science in order to someday work for these companies or even start my own entrepreneurial journey!

# Building a search engine from scratch
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
Web crawlers are programs that exploit the graph strucutre of the Web to move from page to page to download and index content of each page. The goal of a web crawler is to learn what each webpage is about so information can be retrieved when it is needed. A web crawler is needed because the web is not a static entity, but a dynamic one that changes frequently. Web pages/links are constantly deleted, changed, moved and created. Web page updates follow a Poisson distribution on average. Search engines such as Google constantly operate a web crawler to get the most up to date and relevant information so they are able to provide the best user experience. This is constantly used in search engine optimization. It goes from one webpage collecting its outlinks, indexing its content, and moving to the next link. This builds our corpus.<br />

While crawling there are a couple details we want to pay attention to:
  1. Crawl all pages with high textual information content
  2. Detect and avoid infinite traps
  3. Detect and avoid sets of similar pages with no information
  4. Detect and avoid dead URLs that return a 200 status but no data
  5. Detect and avoid crawling very large files, especially if they have low information value

**A Queue (Frontier)**<br />
A frontier is a to-do list for the crawler that contains the URLS of unvisited pages. I used a queue for a FIFO BFS to avoid being stuck in one region for too long and being more fair to other urls. A search engine like Google will probably store their frontier on disk with the amount of URLs they encounter, but I put mine in memory for simplicity sake.

**Limited size of memory in frontier**<br />
Since I only had a limited memory for my frontier, I would need to be a little bit selective of the URLs I chose, ignoring duplicate urls. Since an in memory search for a duplicate URL would have been costly, I allocated some memory for a hashtable/ set to quickly store and check in constant time for duplicates. I could have also implemented the frontier itself as a hashtable to avoid duplicates, but it would have required unnecessary work and time to keep track of the next/ earliest timestamp URL to crawl next.  

**HTTP Client**<br />
In order to fetch a web page, we would need a HTTP client that sends a request for a page and reads a response. I simply used the built in python request module to satisfy this requirement. 

**Initial Seed URLs**<br />
The crawler always needs some place to start, so I initialized the queue with five different University of California Irvine URLs (my university). 

**Politeness and Robot Exclusion**<br />
We first read the webpages robot exclusion protocol and appended their policies to our exclusion list to make sure we do not break the rules and get banned. 

**HTML Parsing**<br />
I decided to use the Beautiful Soup HTML parser because it gave me all of the functionalities I needed, utilizing LXML behind the scenes for speed, and is quite easy to use. It also has built in functionality for tidying up a “dirty” HTML document that is missing tags and etc. Some of the functionalities I needed were the CSS/HTML selectors to easily select the needed elements of a document such as links. It also gave me direct access to tags, such as a header for relevant information. I chose this over the built in python HTML parser because there were no advanced functionalities that were geared to handle HTML and their functions aren’t as up to date as other libraries. I chose this over HTML5lib or HTML5-parser because of speed. Since HTML5lib is written in python and not C, there is a significantly slower.<br />

**Links**<br />
The first thing my parser did was return all of the outlinks from this webpage. All of the returned URLs were then converted to absolute URLs using the base URL to avoid fetching the same page many times. Below are the steps:
	1. Converting the URl to all lowercase.
	2. Removing the anchor or fragment part of the URL, http://myspiders.biz.uiowa.edu/faq.html#what is reduced to http://myspiders.biz.uiowa.edu/faq.html.

**Anatomy of a URL**<br />
A URL is divided into multiple sections:
	1. Web server
	2. Domain
	3. Path
	4. Query
Each link was also matched against the previously picked up URL based off length intersection to avoid picking up slightly different links that all lead to the same page.

**Content**<br />
Stopwords and stemming.<br />
I researched and gathered the top 50 most commonly used words and stopwords when extracting text from a webpage so it will not influence the score of the page. Some stopwords would include: “an”, “to”, “from”, and etc. The reason for this is because a lot of english text contains a lot of repetitive unnecessary words that do not add that much value. This is how compression works because english text is so predictable, it is often able to just remove them entirely or just have their start/end letters. The english word ‘the’ is the most repetitive word in the English language. When encountering words, I would stem them to normalize words. This would mean reducing morphologically similar words to their root word. “Running”, “runs”, and “ran” would all be reduced to “run”. This will greatly help in the scoring process. I used the **porter stemming algorithm**. The porter stemming algorithm** is an algorithm that removes stems of words such as agreed to agree based on its rules.

Same exact/ similar webpage content.<br />
For the same exact webpage content, I used the a crc library hash function to assign each webpage a hash number, append it to our hashtable, and checked against all other webpages to avoid recrawling the same webpage. Cyclic redundancy check (CRC) is a hash function that hashes a stream of bytes with as few collisions as possible.

Similar webpage content.<br />
I implemented my own sim hash function to assign a hash number to the webpage, append it to my sim hashtable, and checked against all other webpages to avoid recrawling a similar webpage. Simhash is a technique that estimates how similar two sets are, one used by Google Crawler. I created mine by creating a fingerprint of each page based on some of the words.

**Robot Exlcusion Protocol**<br />
The robot exclusion protocol is a mechanism that allows web server administrators to communicate their file access policies to identify files that may not be accessed by a crawler. A URL that starts with a value of a disallowed field must not be retrieved by a crawler. Almost all webpages have these policies under the root directory named, robots.txt.

**Avoiding Traps**<br />
A spider trap is a large number of different URLs that refer to the same page. This can be a URL with a calendar and 28+links for each day that lead back to the same calendar. I had a timeout method for my crawler that if it spent more than 5 seconds on the same URL, it would exit and go to the next webpage. This also served beneficial for slow servers or large pages. Another way would be to make sure that only a consecutive sequence of size k, maybe a 100 can be picked up by the crawler. 

**Politeness**<br />
Politeness is not sending multiple requests to the same website over a certain period of time overloading the server which may eventually lead to a DOS(Denial of Service) attack. In my code, there was a 500 ms delay between each request.


# Algorithms
