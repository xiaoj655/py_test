import configparser
import sys,os
import requests
from utils.http_requests import http
import pytest

if __name__=='__main__':
    pytest.main(['-vs', 'test_demo', '--aluredir=./output'])