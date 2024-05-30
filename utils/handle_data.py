from faker import Faker
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import random
import configparser

fake = Faker(locale='zh_CN')
def get_body(api_cfg: configparser, api_path):
    if api_path[0] == '/':
        api_path = api_path[1:]

    return dict(api_cfg.items(api_path+'#body'))

def mock_data(data):
    ret = {}
    for k,v in data.items():
        if ',' in v:
            _v = v.split(',')
            val = random.choice(_v).strip()
        else:
            val = getattr(fake, v)()
        ret.update({k:val})
    return ret

def main(api_cfg:configparser, api_path):
    '''
        pass api_path like '/ac_paper'
        return mock body data of request depend on config
    '''
    d = get_body(api_cfg, api_path)
    d = mock_data(d)
    return d

def compare_dict(a:dict, b:dict):
    '''
        比较a是否是b的子集
        compare a is a sub-collection of b
    '''
    k = a.keys()
    for x in k:
        if(x in b and a[x] == b[x]):
            continue
        else:
            print(f'{a[x]} is different from {b[x]}')
            return False
    return True
