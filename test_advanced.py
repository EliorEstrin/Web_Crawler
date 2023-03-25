from web_crawler import WebCrawler
from bs4 import BeautifulSoup
import requests
import re
import os
from testdata import URL, SECOND_URL, pages

# Not a test
def get_excpected_file_name(depth=0, url=""):
    """
    function gets a url depth and returns the expected name of the file(legal name to the file system).
    for example: the url "www.python.com"" >> www_python_com.html
    """
    valid_url = re.sub(r"https?://", '', url)
    valid_url = re.sub(r'[<>\.:\"/\\|?*]', '_', valid_url) #regex to match all illegar characters in a file
    # replace
    if valid_url[-1] == '_':
        valid_url = valid_url[:-1] # remove the / at the end of a url
    return f"{depth}/{valid_url}.html"


# Not a test
def create_and_run_WebCrawler_object(url, depth, maximal_amount=1, unique_url=False):
    my_crawler = WebCrawler(url, depth=depth, maximal_amount=maximal_amount, unique_url=unique_url)
    my_crawler.run()


def test_object_can_fetch_html_when_depth_one():
    """
    the tests run agains a website that not changes.
    the data for the tests is declared at top
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


def test_object_can_fetch_3_vaild_html_when_depth_one():
    """
    setting maximal amount=3
    expecting in folder /1 to have 3 files with the correct name and html
    the url that are should be found is:
    """
    create_and_run_WebCrawler_object(SECOND_URL, depth=1, maximal_amount=3)

    expected_file_name_0 = get_excpected_file_name(0, SECOND_URL)
    expected_file_name_1 = get_excpected_file_name(1,pages[0]['links'][0]['url'])
    expected_file_name_2 = get_excpected_file_name(1,pages[0]['links'][1]['url'])

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


def test_object_saves_only_unique_files_depth_1():
    create_and_run_WebCrawler_object(SECOND_URL, depth=1, maximal_amount=4, unique_url=True)
    # depth 0 test
    expected_file_name_depth_0 = get_excpected_file_name(0, SECOND_URL)
    # depth 1 , should contain 4 diffrent links
    expected_file_name_depth_1_0 = get_excpected_file_name(1, pages[0]['links'][0]['url'])
    expected_file_name_depth_1_1 = get_excpected_file_name(1, pages[0]['links'][1]['url'])
    expected_file_name_depth_1_2 = get_excpected_file_name(1, pages[0]['links'][3]['url'])
    expected_file_name_depth_1_3 = get_excpected_file_name(1, pages[0]['links'][5]['url'])
    print(expected_file_name_depth_1_0)
    assert os.path.isfile(expected_file_name_depth_0)
    
    assert os.path.isfile(expected_file_name_depth_1_0)
    assert os.path.isfile(expected_file_name_depth_1_1)
    assert os.path.isfile(expected_file_name_depth_1_2)
    assert os.path.isfile(expected_file_name_depth_1_3)


