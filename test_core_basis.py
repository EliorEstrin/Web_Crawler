import pytest
import os
from test_advanced import URL, SECOND_URL, pages, create_and_run_WebCrawler_object, get_excpected_file_name
from bs4 import BeautifulSoup
import requests
################# Core Tests ###############

def test_object_can_create_folders_when_depth_0():
    """
    Test if WebCrawler creates the folders.
    folders should be named as depth
    """
    create_and_run_WebCrawler_object(URL, depth=0)
    assert os.path.isdir('0')


def test_object_can_create_folders_when_depth_bigger_than_zero():
    """
    Test if WebCrawler creates the folders.
    folders should be name 0-int(depth)
    """
    create_and_run_WebCrawler_object(URL, depth=2)
    assert os.path.isdir('0')
    assert os.path.isdir('1')
    assert os.path.isdir('2')


def test_object_can_create_file_with_valid_name_when_depth_zero():
    """
    Valid Name is a name thah can be saved in the Operating System file system
    """
    create_and_run_WebCrawler_object(URL, depth=0)
    expected_file_name = get_excpected_file_name(0, URL)
    assert os.path.isfile(expected_file_name)


def test_object_can_create_file_with_valid_name_when_no_www_in_URL_and_depth_zero():
    """
    Valid Name is a name thah can be saved in the Operating System file system.
    testing against a url without www
    """
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
    assert soup.prettify() == expected_html
