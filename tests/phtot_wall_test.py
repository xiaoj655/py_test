from .base import BaseTestCase
from utils.handle_data import mock_data_by_ali, compare_dict
import pytest
import logging

example = {
  "title": "string",
  "image": "string",
}

base_url = 'http://acm.sztu.edu.cn:55081/api/photo_wall'

_id = None

@pytest.fixture(scope="module")
def data():
    d = mock_data_by_ali(example)
    d.update({"userx_key": '202200202138'})
    return d

class TestAcPaper(BaseTestCase):
    def test_post(self, data):
        ret = self.post(base_url , json=data).json()
        assert ret['status_code'] == 200, f'status code error {ret}'
        global _id
        _id = ret['data']['id']
    
    def test_get(self, data):
        ret = self.get(base_url, params={"id": _id}).json()['data']
        assert compare_dict(data, ret)

    def test_delete(self):
        ret =self.delete(base_url, params={"id": _id}).json()
        assert ret['status_code'] == 200, f'delete error {ret.text}'
