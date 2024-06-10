from .base import BaseTestCase
from utils.handle_data import mock_data_by_ali, compare_dict
import pytest

example = {
    "bib_kind": "article",
    "b_author": "name",
    "b_booktitle": "word",
    "b_title": "word",
    "b_journal" : "word",
    "b_publisher" : "word",
    "b_year": "2001",
}
base_url = 'http://acm.sztu.edu.cn:55080/api/ac_paper'

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
        ret = self.get(base_url, params={"id": _id}).json()
        assert compare_dict(data, ret)

    def test_delete(self):
        ret =self.delete(base_url, params={"id": _id}).json()
        assert ret['status_code'] == 200, f'delete error {ret.text}'
