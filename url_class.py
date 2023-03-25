import os
import requests
from bs4 import BeautifulSoup
import re


class WebCrawler:

    def __init__(self, url, maximal_amount=1, depth=0):
        self.url = url
        self.depth = str(depth)
        self.maximal_amount = maximal_amount # maximal amount of links per page
        

    def get_valid_file_name(self,url_to_validate):
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
    def create_folders(self):
        for folder_name in range(int(self.depth) + 1):
            if not os.path.exists(str(folder_name)):
                os.mkdir(str(folder_name))


    def get_html_as_soup(self,url_to_fetch):
        response = requests.get(url_to_fetch)
        soup = BeautifulSoup(response.text, "html.parser")
        # print(soup.prettify())
        return soup

    def create_html_files(self,current_url,depth=0):
        if int(depth) > int(self.depth):
            return "Files has been created"
        else:
            # saving the current_url with valid name and .html suffix at the end
            file_path = f"{depth}/{self.get_valid_file_name(current_url)}.html"
            current_page = ""
            with open(f"{file_path}", "w", encoding='utf-8') as file:
                current_page = self.get_html_as_soup(current_url)
                file.write(str(current_page.prettify()))

            # Extract new URLs from the HTML content and run the function recursivly on them
            # prevents the running to not scan urls that are not going to be used
            if int(depth) < int(self.depth):
                new_urls = self.search_for_links(page_html=current_page.prettify())
                for link in new_urls:
                    self.create_html_files(link, depth + 1)
                
    def search_for_links(self, page_html):
        counter = 0
        links = []

        # print all a href links from a page
        soup = BeautifulSoup(page_html, 'html.parser')
        # soup = self.get_html_as_soup()
        # print(soup.find_all('a'))
        for link in soup.find_all('a'):
            if counter >= self.maximal_amount:
                break
            # print(link.get('href'))
            if link.get('href') is not None:
                link = link.get('href')
                
                # only links of https/http
                if link.startswith("https://") or link.startswith("http://"):
                    counter += 1
                    links.append(link)
                    print(link)
        return links

    def run(self):
        self.create_folders()
        # start running 
        self.create_html_files(self.url)

