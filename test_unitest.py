import pytest
import os
from url_class import Url
from bs4 import BeautifulSoup
import requests

URL='https://www.pythontutorial.net/' # Url used to test functions
SECOND_URL =  "https://justdvir.online/" # Url without www


def create_and_run_url_object(url, depth):
    my_url = Url(url, depth=depth)
    my_url.run()


def test_can_create_folders_as_depth_0():
    """
    depth n should mean n + 1 directories should exist in an incresing order 
    depth = 0 > 1 dir
    depth = 1 > 2 dir (0,1)
    """
    create_and_run_url_object(URL, depth=0)
    assert os.path.isdir('0')


def test_can_create_folders_as_depth_bigger_than_zero():
    create_and_run_url_object(URL, depth=2)
    assert os.path.isdir('0')
    assert os.path.isdir('1')
    assert os.path.isdir('2')


def test_can_create_file_with_valid_name_with_depth_zero():
    create_and_run_url_object(URL, depth=0)
    expected_file_name = f'0/www_pythontutorial_net.html'
    assert os.path.isfile(expected_file_name)

def test_can_create_file_with_valid_name_no_www_depth_zero():
    create_and_run_url_object(SECOND_URL , depth=0)
    expected_file_name = f'0/justdvir_online.html'
    assert os.path.isfile(expected_file_name)


def test_can_save_the_correct_html_depth_zero():
    create_and_run_url_object(URL, depth=0)

    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")

    # Read the HTML file into a string
    with open('0/www_pythontutorial_net.html', 'r') as f:
        expected_html = f.read()
    assert soup.prettify() == expected_html

# def test_can_save_the_correct_html_depth_one():
#     create_and_run_url_object(URL, depth=1)

