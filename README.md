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
[Stopwords and stemming.<br />](https://gist.github.com/sebleier/554280)
I researched and gathered the top 50 most commonly used words and stopwords when extracting text from a webpage so it will not influence the score of the page. Some stopwords would include: “an”, “to”, “from”, and etc. The reason for this is because a lot of english text contains a lot of repetitive unnecessary words that do not add that much value. This is how compression works because english text is so predictable, it is often able to just remove them entirely or just have their start/end letters. The english word ‘the’ is the most repetitive word in the English language. When encountering words, I would stem them to normalize words. This would mean reducing morphologically similar words to their root word. “Running”, “runs”, and “ran” would all be reduced to “run”. This will greatly help in the scoring process. I used the **porter stemming algorithm**. The porter stemming algorithm** is an algorithm that removes stems of words such as agreed to agree based on its rules.

[Same exact/similar webpage content.<br />](https://docs.python.org/3/library/hashlib.html)
For the same exact webpage content, I used the a CRC library hash function to assign each webpage a hash number, append it to our hashtable, and checked against all other webpages to avoid recrawling the same webpage. Cyclic redundancy check (CRC) is a hash function that hashes a stream of bytes with as few collisions as possible.

[Similar webpage content.<br />](https://en.wikipedia.org/wiki/SimHash)
I implemented my own sim hash function to assign a hash number to the webpage, append it to my sim hashtable, and checked against all other webpages to avoid recrawling a similar webpage. Simhash is a technique that estimates how similar two sets are, one used by Google Crawler. I created mine by creating a fingerprint of each page based on some of the words.

**Robot Exlcusion Protocol**<br />
The robot exclusion protocol is a mechanism that allows web server administrators to communicate their file access policies to identify files that may not be accessed by a crawler. A URL that starts with a value of a disallowed field must not be retrieved by a crawler. Almost all webpages have these policies under the root directory named, robots.txt.

**Avoiding Traps**<br />
A spider trap is a large number of different URLs that refer to the same page. This can be a URL with a calendar and 28+links for each day that lead back to the same calendar. I had a timeout method for my crawler that if it spent more than 5 seconds on the same URL, it would exit and go to the next webpage. This also served beneficial for slow servers or large pages. Another way would be to make sure that only a consecutive sequence of size k, maybe a 100 can be picked up by the crawler. 

**Politeness**<br />
Politeness is not sending multiple requests to the same website over a certain period of time overloading the server which may eventually lead to a DOS(Denial of Service) attack. In my code, there was a 500 ms delay between each request.

# The Inverted Index

**What is an inverted index?**<br />
It is simply a map with token as a key and a list of its corresponding postings where a posting may contain the token's frequency within a document, documenty id the token was found in, tokens position, and tf-idf score of that document It is the step that occurs after crawling where crawling scans the web returning each website's url and content of that url. It is called inverted because the keys are words while the values are the document's information.

**What is the goal of an inverted index?**<br />
The goal of an inverted index is to provide fast lookup times for the search engine and return URLs based on relvancy based on the query.

**Why is an inverted index needed?**<br />
An inverted index is required because it would take too much time to scan over documents, calculating its tf-idf score to the query and returning relevant results in real time compared to just preprocessing all of the data.

**Implementation**<br />
After crawling and storing all of the websites in to disk, I would iterate over each document, parse it, get the frequency of each word and their positions relative to the document, and write it out to file. Since there were so many files, I had to write it out to disk instead of saving it within memory. After each iteration, I would save it in memory, but after the 5000th iteration, I would write it out to file, clear it in memory, and restart until I was done with all of the documents. Since an in-memory seasrch for a duplicate URL would have been costly, I allocated some mory for a hashtable to quickly store and check in constant time for duplicates and similar webpages using CRC check and Simhash checking.

# Search Engine
**What is a search engine?**<br />
Once the crawling and indexing is done, a query is given to a search engine and the search engine is supposed to presnt the most relevant documents back to that query.


**Ranking Algorithms**<br />
[Boolean Search](https://www.nypl.org/blog/2011/02/22/what-boolean-search#:~:text=Boolean%20searching%20is%20built%20on,broaden%2C%20or%20define%20your%20search.): The problem with a boolean search is that it is either results in too many documents or too few.

[Jaccard coefficient](https://en.wikipedia.org/wiki/Jaccard_index): The set intersection between the query and documents. It doesn't consider term frequency (how many times a term occurs in a document). Rare terms in a collection are more informative than frequent terms. Jaccard doesn't consider this information

[TF-IDF](https://en.wikipedia.org/wiki/Tf%E2%80%93idf): term frequency * inverse document frequency. Best known and most widely using weighting scheme in IR. 

[N-gram indexing](https://whoosh.readthedocs.io/en/latest/ngrams.html): Compares the positions of terms within a query to the positions of terms within a document. If trhere is a document with terms in the exact same position as the query, it wouyld be ranked higher than other documents.

[Google's PageRank](https://en.wikipedia.org/wiki/PageRank): Pagerank is another weighting of documents that would give a document more weight if it had a lot of inlinks compared to one document that doesn't have a lot of inlinks.
Algorithm:
  1. Start on a random page
  2. Visit one of the outlinks based of equal probability
  3. Keep on doing this until we reach a steady state of long term visit rates and use this as part of the rating, similar to a steady state of a markov chain.
  4. However, this random walk could result in dead end pages, so with 10 % probability jump to any random page.<br />
  5. We record the amount of visits a page gets and logically a page that gets visited more would be more important<br />

**Retrieving relevant information based on cosine similarity**<br />
Ranking documents in decreasing order of angle(query, document) is the same as ranking documents in increasing order of cosine(query, document):
  1. Take the tf-idf score of both the query and document, for the document all of it is done beforehand, preprocessing.
  2. Normalize the tf-idf score using length normalization
  3. Take cosine similarity of both of these scores using the dot product
  4. We repeat for each term within the query and sum it all up
  5. Return the top 10 highest similar results, largest query-doc cosines.
  6. Pretty much solving the K-nearest neighbors for a query vector


