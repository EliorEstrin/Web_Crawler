import os
import requests
from bs4 import BeautifulSoup
import re
from status_printer import StatusPrinter
class WebCrawler:

    def __init__(self, url, maximal_amount=1, depth=0, unique_url=False):
        """
        Initializes the WebCrawler object with the specified parameters.

        Args:
            url (str): The starting URL for the crawl.
            maximal_amount (int): The maximum number of links to follow from each page.
            depth (int): The maximum depth to crawl from the starting URL.
            unique_url (bool): Whether to only download each unique URL once.
        """
        self.url = url
        self.depth = str(depth)
        self.maximal_amount = maximal_amount # maximal amount of links per page
        self.unique = bool(unique_url)
        self.downloaded_urls = []
        self.maximal_exceptions = 5
        self.current_exceptions = 0
        self.status_printer = StatusPrinter()

    def send_request(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching {url}: {e}")
            return None
        return response

    def sanitize_filename(self, url_to_validate):
        """
        The function validates the URL before saving the file
        remove https from the begging 
        <depth>/<url>.html
        the url must not contain: /   ? * '' < > 
        if any of illegar charactes apper it is replaced with _
        """
        valid_url = re.sub(r"https?://", '', url_to_validate)
        valid_url = re.sub(r'[<>\.:\"/\\|?*]', '_', valid_url) #regex to match all illegar characters in a file
        valid_url = valid_url.rstrip('_')
        return valid_url

    # Should be private
    def create_directory_structure(self):
        """
        Create the necessary directory structure for the specified
        depth if the directories do not already exist.
        """
        for folder_name in range(int(self.depth) + 1):
            if not os.path.exists(str(folder_name)):
                os.mkdir(str(folder_name))

    def fetch_soup_from_url(self, url_to_fetch):
        """
        Fetches the HTML content from the specified URL and returns a BeautifulSoup object.
        """
        response = self.send_request(url_to_fetch)
        if response is not None:
            soup = BeautifulSoup(response.text, "html.parser")
            return soup
        return None

    def download_html_content(self, current_url, depth=0):
        """
        Downloads the HTML content of the specified URL and saves it to a file.
        Then extracts new URLs from the HTML content and runs the function recursively on them.
        :param current_url: The URL to download.
        :param depth: The current depth of the crawl.
        """
        # Exit if to many exceptions occurded
        if self.current_exceptions >= self.maximal_exceptions:
            return None

        current_page = self.fetch_soup_from_url(current_url)
        file_path = f"{depth}/{self.sanitize_filename(current_url)}.html"

        # StdOut status messages
        self.status_printer.print_depth(depth)
        self.status_printer.print_url(current_url)

        if current_page is not None:
            with open(f"{file_path}", "w", encoding='utf-8') as file:
                self.status_printer.print_file(file_path)
                file.write(current_page.prettify())
                self.downloaded_urls.append(current_url)
        else:
            self.current_exceptions += 1
            # if the file is None exepction occured
            # Possible to raise value error

        # A Check wether the scanning of urls should continue
        depth_in_range = int(depth) < int(self.depth)
        if depth_in_range:
            if current_page is not None:
                new_urls = self.search_for_links(page_html=current_page.prettify())
                for link in new_urls:
                    self.download_html_content(link, depth + 1)

    def search_for_links(self, page_html):
        """
        Search for links in the given HTML content and return a list of links.
        The maximal amount of links to return can be set with the maximal_amount parameter.
        If unique_url is set to True, only unique URLs are returned.
        """
        soup = BeautifulSoup(page_html, 'html.parser')
        # Save into links all links that start with https, http
        links = [link.get('href').rstrip('/') for link in soup.find_all('a') 
             if link.get('href') and re.match(r'^https?://', link.get('href'))]

        if self.unique:
            # Make sure the links in the list unique
            links = list(set(links) - set(self.downloaded_urls))[:self.maximal_amount]
        else:
            links = links[:self.maximal_amount]
        return links

    def report_status(self):
        status = self.current_exceptions < self.maximal_exceptions
        if status:
            print("Crawler Finished Running")
            # exit 0
        else:
            print(f"Crawler failed: maximum number of exceptions ({self.maximal_exceptions}) exceeded")

    def run(self):
        """
        Run the web crawler to download webpages and save them as HTML files.
        """
        self.create_directory_structure()
        # start running
        self.download_html_content(self.url)
        self.report_status()
