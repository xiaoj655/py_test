from utils.http_requests import HttpRequest
import pytest

class BaseTestCase(HttpRequest):
    @pytest.fixture(scope='class', autouse=True)
    def setup_class(self):
        self.login()