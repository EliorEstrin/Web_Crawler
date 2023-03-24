import pytest
import os
from url_class import Url
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

# def test_can_create_file_with_valid_name():
#     URL='https://www.pythontutorial.net/'
#     my_url = Url(f"{URL}", depth=0)
#     expected_file_name = f'0/www_pythontutorial_net.html'
#     assert os.path.isfile(expected_file_name)
