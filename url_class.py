import os
import requests
from bs4 import BeautifulSoup
import re


class Url:

    def __init__(self, url, maximal_amount=1, depth=0):
        self.url = url
        self.depth = str(depth)
        print(os.path.exists(self.depth))


    def get_valid_file_name(self):
        """
        The function validates the URL before saving the file
        remove https from the begging 
        <depth>/<url>.html
        the url must not contain: /   ? * '' < > 
        if any of illegar charactes apper it is replaced with _ 
        """
        valid_url = re.sub(r'[^\w\-_.]', '_', self.url)
        # remove the / at the end of a url
        if valid_url[-1] == '_':
            valid_url = valid_url[:-1]

        valid_url = re.sub(r'https?://', '', valid_url)
        return valid_url
    
    def create_folders(self):
        for folder_name in range(int(self.depth) + 1):
            if not os.path.exists(str(folder_name)):
                print("creting a folder")
                os.mkdir(str(folder_name))

    # def save_file(self):
    #     file_path = f"{self.depth}/{self.get_valid_file_name()}.html"
    #     print(file_path)
    #     with open(f"{file_path}", "w", encoding='utf-8') as file:
    #         soup = self.scan_and_save_page()
    #         file.write(str(soup.prettify()))

    # def scan_and_save_page(self):
    #     response = requests.get(self.url)
    #     soup = BeautifulSoup(response.text, "html.parser")
    #     print(soup.prettify())
    #     return soup
    def run(self):
        self.create_folders()
