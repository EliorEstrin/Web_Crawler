import pytest
import os
from url_class import WebCrawler
from bs4 import BeautifulSoup
import requests
import re

# URSL used for testing
URL = 'https://www.pythontutorial.net/' # WebCrawler used to test functions
SECOND_URL = "https://justdvir.online/" # WebCrawler without www

# Example for a page with links inside that used in the testing
pages = [
    {
        'url': 'https://justdvir.online/',
        'links': [
            {'text': 'Link 1', 'url': 'https://www.linkedin.com/in/dvir-pashut-477992249/'},
            {'text': 'Link 2', 'url': 'https://github.com/dvir-pashut/portfolio-'},
            {'text': 'Link 3', 'url': 'https://github.com/dvir-pashut/portfolio-'},
            {'text': 'Link 4', 'url': 'https://persona-generator.today'},
            {'text': 'Link 4', 'url': 'https://persona-generator.today/'},
            {'text': 'Link 4', 'url': 'https://www.credly.com/badges/cd7f11f6-73b2-47dc-b5df-b737ef61a0fe/linked_in?t=rlwl2i'}
        ]
    },
]


def get_excpected_file_name(depth=0, url=""):
    """
    function gets a url depth and returns the expected name of the file.
    for example: the url "www.python.com"" >> www_python_com.html
    """
    valid_url = re.sub(r"https?://", '', url)
    valid_url = re.sub(r'[<>\.:\"/\\|?*]', '_', valid_url) #regex to match all illegar characters in a file
    # replace
    if valid_url[-1] == '_':
        valid_url = valid_url[:-1] # remove the / at the end of a url
    return f"{depth}/{valid_url}.html"


def create_and_run_WebCrawler_object(url, depth, maximal_amount=1):
    my_crawler = WebCrawler(url, depth=depth, maximal_amount=maximal_amount)
    my_crawler.run()


def test_object_can_create_folders_when_depth_0():
    """
    depth n should mean n + 1 directories should exist in an incresing order 
    depth = 0 > 1 dir
    depth = 1 > 2 dir (0,1)
    """
    create_and_run_WebCrawler_object(URL, depth=0)
    assert os.path.isdir('0')


def test_object_can_create_folders_when_depth_bigger_than_zero():
    create_and_run_WebCrawler_object(URL, depth=2)
    assert os.path.isdir('0')
    assert os.path.isdir('1')
    assert os.path.isdir('2')


def test_object_can_create_file_with_valid_name_when_depth_zero():
    create_and_run_WebCrawler_object(URL, depth=0)
    expected_file_name = get_excpected_file_name(0, URL)
    assert os.path.isfile(expected_file_name)


def test_object_can_create_file_with_valid_name_when_no_www_in_URL_and_depth_zero():
    create_and_run_WebCrawler_object(SECOND_URL, depth=0)
    expected_file_name = get_excpected_file_name(0, SECOND_URL)
    assert os.path.isfile(expected_file_name)


def test_object_can_save_the_correct_html_when_depth_zero():
    create_and_run_WebCrawler_object(URL, depth=0)

    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")

    # Read the HTML file into a a string and assert that is equal to what inside the file
    expected_file_name = get_excpected_file_name(0, URL)
    with open(expected_file_name, 'r') as f:
        expected_html = f.read()
    # with open('0/www_pythontutorial_net.html', 'r') as f:
    #     expected_html = f.read()
    assert soup.prettify() == expected_html

def test_object_can_fetch_html_when_depth_one():
    """
    the tests run agains a website that not changes
    the first link should be: https://www.linkedin.com/in/dvir-pashut-477992249/
    means the file name should be named: www_linkedin_com_in_dvir-pashut-477992249.html
    and maximal amount = 1
    """
    create_and_run_WebCrawler_object(SECOND_URL, depth=1)
    # asserting both depth 0 and 1
    expected_file_name_0 = get_excpected_file_name(0, SECOND_URL)
    expected_file_name_1 = get_excpected_file_name(1, pages[0]['links'][0]['url'])


    assert os.path.isfile(expected_file_name_0)
    assert os.path.isfile(expected_file_name_1)

    # Asserting that the file have the corret html inside
    response_1 = requests.get(SECOND_URL)
    response_2 = requests.get(pages[0]['links'][0]['url'])

    soup_0 = BeautifulSoup(response_1.text, "html.parser")
    soup_1 = BeautifulSoup(response_2.text, "html.parser")

    # depth 0
    with open(expected_file_name_0, 'r') as f:
        expected_html = f.read()
    assert soup_0.prettify() == expected_html

    # depth 1
    with open(expected_file_name_1, 'r') as f:
        expected_html = f.read()
    assert soup_1.prettify() == expected_html

def test_object_can_fetch_more_than_one_html_when_depth_one():
    """
    setting maximal amount=3
    expecting in folder /1 to have 3 files with the correct name and html
    the url that are should be found is:

    """
    create_and_run_WebCrawler_object(SECOND_URL, depth=1, maximal_amount=3)
    
    # asset dir 0 exists with correct file
    expected_file_name_0 = get_excpected_file_name(0, SECOND_URL)

    # assert dir 1 exists with correect 3 files and correct html inside 2 url is the same link        .
    expected_file_name_1 = get_excpected_file_name(1,pages[0]['links'][0]['url'])
    # expected_file_name_1 = get_excpected_file_name(1,'https://www.linkedin.com/in/dvir-pashut-477992249/')
    expected_file_name_2 = get_excpected_file_name(1,pages[0]['links'][1]['url'])
    # expected_file_name_2 = get_excpected_file_name(1,'https://github.com/dvir-pashut/portfolio-')

    assert os.path.isfile(expected_file_name_0)
    assert os.path.isfile(expected_file_name_1)
    assert os.path.isfile(expected_file_name_2)
    
    excpected_links = [SECOND_URL, pages[0]['links'][0]['url'], pages[0]['links'][1]['url']]
    excpected_responses = []

    for link in excpected_links:
        response = requests.get(link)
        soup = BeautifulSoup(response.text, "html.parser")
        excpected_responses.append(soup)

    # asseting the html response
    with open(expected_file_name_0, 'r') as f:
        excpected_html = f.read()
    assert excpected_responses[0].prettify() == excpected_html

    with open(expected_file_name_1, 'r') as f:
        excpected_html = f.read()
    assert excpected_responses[1].prettify() == excpected_html
    
    with open(expected_file_name_2, 'r') as f:
        excpected_html = f.read()
    # each github page has uniqu identifier means a two page never will be the same
    assert excpected_responses[2].prettify()[:100] == excpected_html[:100]
