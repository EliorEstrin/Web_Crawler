import pytest
import os

# from url_class import Url
from url_class import Url

# URL='http://localhost.com/'

# easy test
def test_can_save_single_html_in_folder():
    """
    expects a '<depth>/URL.html' folder created with valid html inside.
    this is an easy test means it only checks for depth=0 which is the 
    default.
    """
    URL='http://localhost.com/'

    my_url = Url(f"{URL}")
    my_url.run()

    expected_file_name = f'0/localhost_com.html'

    assert os.path.isdir('0')
    assert os.path.isfile(expected_file_name)
    # assert os.path.isfile(expected_file_nae)

# def file_exist(
