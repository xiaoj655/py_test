import configparser
import pytest
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.handle_data import main
import utils.handle_data
from utils.http_requests import HttpRequest
from config import cfg
import requests

api_cfg = configparser.ConfigParser()
api_cfg.read(os.path.join(os.path.dirname(__file__), 'api.cfg'))
d = main(api_cfg, '/ac_paper')
id = ''

@pytest.fixture
def id():
    global id
    return id

@pytest.fixture
def data():
    return d

class TestDemo():
    def setup_method(self):
        self.http = HttpRequest()
        self.http.login()
        self.path = self.merge_path('/ac_paper')
    
    def merge_path(self, path):
        return cfg.get('api', 'base_url') + path
    
    def test_post(self, data):
        ret = self.http.post(
            self.path,
            json=data,
            headers={"Content-Type": "application/json"}
            )
        global id
        id = ret.json()['data']['id']

    def test_get(self, id):
        ret = self.http.get(self.path, params={"id": id})
        verify = utils.handle_data.compare_dict(d, ret.json())
        assert verify
    
    def test_put(self, id):
        d2 = main(api_cfg, '/ac_paper')
        d2.update({"userx_key": '202200202138'})
        ret = self.http.put(self.path, params={"id": id}, json=d2).json()
        verify = utils.handle_data.compare_dict(d2, ret['data'])
        assert verify
    
    def test_delete(self, id):
        ret = self.http.delete(self.path, params={"id": id})
        assert ret['status_code'] == 200
