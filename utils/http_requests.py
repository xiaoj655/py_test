import requests
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import cfg


class HttpRequest():
    def __init__(self):
        self.headers = {}
        self.session = requests.Session()
    
    def login(self):
        sso_token = self.session.post(
            cfg.get('auth', 'sso_path'),
            json={
                "user_id": cfg.get('auth', 'user_id'),
                "password": cfg.get('auth', 'password')
                }
        )
        sso_token = sso_token.json()['access_token']
        token = self.session.get(cfg.get('auth', 'login_path') + sso_token)
        token = token.json()['access_token']
        self.set_token(token)
    
    def set_token(self, token):
        self.token = token
        self.headers.update({
            "Authorization": token
        })
    
    def get(self, path, params, headers={}):
        headers.update(self.headers)
        ret = self.session.get(params, headers=headers)
        return ret.json()
    
    def post(self, path, params,data=None, json=None, headers={}):
        headers.update(self.headers)
        ret = self.session.post(
                 path, data=data, json=json,params=params, headers=headers
                )
        return ret.json()

http = HttpRequest()