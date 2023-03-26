import os
import requests
from bs4 import BeautifulSoup
import re


class WebCrawler:

    def __init__(self, url, maximal_amount=1, depth=0, unique_url=False):
        self.url = url
        self.depth = str(depth)
        self.maximal_amount = maximal_amount # maximal amount of links per page
        self.unique = bool(unique_url)
        self.downloaded_urls = [self.url]
        self.maximal_exceptions = 5
        self.current_exceptions = 0

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
        if valid_url[-1] == '_':
            valid_url = valid_url[:-1] # remove the / at the end of a url
        return valid_url

    # Should be private
    def create_directory_structure(self):
        for folder_name in range(int(self.depth) + 1):
            if not os.path.exists(str(folder_name)):
                os.mkdir(str(folder_name))

    def fetch_soup_from_url(self, url_to_fetch):
        response = self.send_request(url_to_fetch)
        if response is not None:
            soup = BeautifulSoup(response.text, "html.parser")
            return soup
        return None

        # response = requests.get(url_to_fetch)
        # soup = BeautifulSoup(response.text, "html.parser")
        # # print(soup.prettify())
        # return soup

    def download_html_content(self, current_url, depth=0):

        if self.current_exceptions >= self.maximal_exceptions:
            return None
        else:
            current_page = self.fetch_soup_from_url(current_url)
            # saving the current_url with valid name and .html suffix at the end
            file_path = f"{depth}/{self.sanitize_filename(current_url)}.html"
            with open(f"{file_path}", "w", encoding='utf-8') as file:
                # current_page = self.fetch_soup_from_url(current_url)
                if current_page is not None:
                    file.write(str(current_page.prettify()))
                else:
                    self.current_exceptions += 1

            # Extract new URLs from the HTML content and run recursibly
            depth_in_range = int(depth) < int(self.depth)
            if depth_in_range:
                if current_page is not None:
                    new_urls = self.search_for_links(page_html=current_page.prettify())
                    for link in new_urls:
                        self.download_html_content(link, depth + 1)


                
    def search_for_links(self, page_html):
        counter = 0
        links = []

        # print all a href links from a page
        soup = BeautifulSoup(page_html, 'html.parser')
        # soup = self.fetch_soup_from_url()
        # print(soup.find_all('a'))
        for link in soup.find_all('a'):
            if counter >= self.maximal_amount:
                break
            # print(link.get('href'))
            if link.get('href') is not None:
                link = link.get('href')
                
                # only links of https/http
                if link.startswith("https://") or link.startswith("http://"):
                    link = link.rstrip('/')
                    links.append(link)
                    
                    # if unique and the url exists counter would be incremented
                    if self.unique and link in self.downloaded_urls:
                        continue
                        self.downloaded_urls = list(set(self.downloaded_urls))
                        # links.append(link)
                        # self.downloaded_urls.append(link)
                    else:
                        self.downloaded_urls = list(set(self.downloaded_urls))
                        self.downloaded_urls.append(link)
                        counter += 1
                           
                    # counter += 1
        return links
    
    def report_status(self):
        status = self.current_exceptions < self.maximal_exceptions
        if status:
            print("Crawler Finished Running")
            # exit 0
        else:
            print(f"Crawler failed: maximum number of exceptions ({self.maximal_exceptions}) exceeded")


    def run(self):
        self.create_directory_structure()
        # start running 
        self.download_html_content(self.url)
        self.report_status()

