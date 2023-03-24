import pytest
import os
from url_class import Url
from bs4 import BeautifulSoup
import requests

# URL='http://localhost.com/'

# easy test 
def test_can_create_folders_as_depth_0():
    """
    depth n should mean n + 1 directories should exist in an incresing order 
    depth = 0 > 1 dir
    depth = 1 > 2 dir (0,1)
    """
    URL='https://www.pythontutorial.net/'
    my_url = Url(f"{URL}", depth=0)
    my_url.run()
    assert os.path.isdir('0')

def test_can_create_folders_as_depth_bigger_than_zero():
    URL='https://www.pythontutorial.net/'
    my_url = Url(f"{URL}", depth=2)
    my_url.run()
    assert os.path.isdir('0')
    assert os.path.isdir('1')
    assert os.path.isdir('2')

def test_can_create_file_with_valid_name_with_depth_zero():
    URL='https://www.pythontutorial.net/'
    my_url = Url(f"{URL}", depth=0)
    expected_file_name = f'0/www_pythontutorial_net.html'
    assert os.path.isfile(expected_file_name)

def test_can_save_the_correct_html():
    URL='https://www.pythontutorial.net/'
    response = requests.get(URL)
    my_url = Url(f"{URL}", depth=0)
    my_url.run()




    soup = BeautifulSoup(response.text, "html.parser")
    # Read the HTML file into a string
    with open('0/www_pythontutorial_net.html', 'r') as f:
        expected_html = f.read()
    assert soup.prettify() == expected_html

