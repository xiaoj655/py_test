from faker import Faker
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import random
import configparser
import dashscope
import json
import re

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
        if(x in b and a[x] == b[x] or str(a[x]) == str(b[x])):
            continue
        else:
            print(f'{a[x]} is different from {b[x]}')
            return False
    return True

# a = {'bib_kind': 'article', 'b_author': 'John Doe', 'b_booktitle': 'Journal of Artificial Intelligence', 'b_title': 'Exploring Deep Learning Techniques for Natural Language Processing', 'b_journal': 'IEEE Transactions on Neural Networks and Learning Systems', 'b_publisher': 'Springer', 'b_year': 2021, 'userx_key': 202200202138}
# b = {'created_at': None, 'updated_at': None, 'addition': None, 'attach_filex': {}, 'id': '55318b8d-3e4d-4f65-b919-b5d9dc5c1636', 'available': True, 'userx_key': '202200202138', 'bib_kind': 'article', 'b_author': 'John Doe', 'b_booktitle': 'Journal of Artificial Intelligence', 'b_title': 'Exploring Deep Learning Techniques for Natural Language Processing', 'b_journal': 'IEEE Transactions on Neural Networks and Learning Systems', 'b_key': None, 'b_number': None, 'b_publisher': 'Springer', 'b_volume': None, 'b_year': '2021', 'b_doi': None, 'b_url': None}
# print(compare_dict(a,b))

def mock_data_by_ali(data):
    if not isinstance(data, str):
        data = json.dumps(data)
    messages = [
        {"role": "system", "content": "请以以下内容为基础, 返回给我一个可用于接口测试的数据, \
            生成的数据类型严格按照输入的类型生成, 只能是字符串类型或数字类型,\
            , 不要回答任何人类语言"},
        {"role": "user", "content": data}
    ]
    ret = dashscope.Generation.call(
        model=dashscope.Generation.Models.qwen_turbo,
        messages=messages,
        result_format='message',
        seed=random.randint(1,10000)
    )
    d = ret['output']['choices'][0]['message']['content']
    return json.loads(parse(d))

def parse(data):
    st = 0
    end = 0
    for x in range(0, len(data)):
        if(data[x] == '{'):
            st = x
    for x in reversed(data):
        if x == '}':
            end = len(data) - end
            break
        else:
            end += 1
    return data[st:end]