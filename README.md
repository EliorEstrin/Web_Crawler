# Web Crawler
This is a software program that downloads HTML content from a starting URL and recursively extracts HTML content from URLs found in the resulting pages. 

# Usage
in order to run Web Crawler you must create a WebCrawler object.
the arguments would be:
1. url - The starting URL for the process.
2. maximal_amount - The maximum number of unique URLs to extract from each page.
3. depth - The depth factor to control how deep the recursion should go.
4. unique_url - A boolean flag indicating whether URLs should be unique across different depths.

then in your app.py you can implement:
```
from web_crawler import WebCrawler

# creating the object
myCrawler = WebCrawler(url="https://example.com", depth=1, maximal_amount=10, unique_url=True)

# starting the webCrawler
myCrawler.run()
```

# File Storage
The HTML content for each downloaded page will be stored in a separate file with the naming convention `<depth>/<url>.html`. <br>
Any characters that are not allowed in file names are replaced with underscores.<br> For example, if the starting URL is `https://www.example.com` and the recursion reaches a depth of 2, the HTML content for the page at `https://www.example.com/page.html` will be stored in the file `2/www_example_com_page_html`.html.

# Dependencies
Get all the program dependencies by running
```
pip install -r requirments.txt
```
# Tests
This program was developed using Test-Driven Development (TDD) methodology, with tests being written before the implementation code. The test files included in this repository are:
- testdata.py: Contains test data for the program.
-  test_advanced.py: Contains advanced level tests for the program, testing edge cases and more complex scenarios.
- test_core_basis.py: Contains basic level tests for the program, testing its core functionality.

