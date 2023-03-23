import pytest
import os


URL='http://localhost.com/'


def test_can_create_file():
    """
    expects a '<depth>/URL'  
    """
    expected_file_name = f'0/localhost_com.html'

    assert os.path.isdir('0')


# def file_exist(
