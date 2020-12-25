import csv
import pystache
import yaml
import json
import os

from collections import OrderedDict


def save_case(record):
    # 保存请求
    path = os.getcwd() + '/' + record['record_name'] + '/'
    j_path = path + record['record_name'] +'_record.json'

    if os.path.exists(j_path):
        with open(j_path, 'r') as f:
            data = json.load(f)
    else:
        data = {}
        data['Config'] = {
            "name":record['record_name'],
            "record":"true",
            "describe":""
        }
        data['TestCase'] = OrderedDict()
    name = record['case_name']+'_'+str(record['index'])
    data['TestCase'][name] = {}
    data['TestCase'][name]['api'] = record['api']
    data['TestCase'][name]['method'] = record['method']
    data['TestCase'][name]['head'] = record['head']
    case = {
        "Sucess": {
            "body": record['body'],
            "story":'',
            "assert": [
                {
                    "value": f"response_diff('{record['record_name']}', '{name}', '{record['api']}', '{record['method']}', r) == ''",
                    "info": "返回数据与预期不符"
                }
            ]
        }
    }
    data['TestCase'][name]['process'] = case
    with open(j_path, 'w') as f:
        f.writelines(json.dumps(data, indent=4, ensure_ascii=False))

    # 保存返回
    r_path = path + '/data/' + record['record_name'] + '_record.json'
    r = {}
    if os.path.exists(r_path):
        with open(r_path, 'r') as f:
            r = json.load(f)
    r[name] = {}
    r[name]['Sucess'] = []
    r[name]['Sucess'].append(record['response'])
    with open(r_path, 'w') as f:
        f.writelines(json.dumps(r, indent=4, ensure_ascii=False))

