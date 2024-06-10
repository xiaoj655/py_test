import requests
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import cfg


class HttpRequest():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Content-Type": "application/json"
    }
    session = requests.sessions.Session()
    
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
            "Authorization": f"Bearer {self.token}"
        })
    
    def get(self, path, params=None, headers={}):
        headers.update(self.headers)
        ret = self.session.get(path, params=params, headers=headers)
        return ret
    
    def post(self, path, params = None,data=None, json=None, headers={}):
        headers.update(self.headers)
        ret = requests.post(
            path,
            json=json,
            data=data,
            params=params,
            headers=headers
        )
        return ret
    
    def delete(self, path, params={}, headers={}):
        headers.update(self.headers)
        ret = self.session.delete(
                 path, params=params, headers=headers
                )
        return ret
    
    def put(self, path, params,json={}, data=None, headers={}, is_json=True):
        headers.update(self.headers)
        ret = self.session.put(
            path,
            params=params,
            data=data,
            headers=headers,
            json=json
        )
        return ret

http = HttpRequest()