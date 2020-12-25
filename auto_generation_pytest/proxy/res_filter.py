import csv
import pystache
import yaml
import json
import os

from pathlib import Path
from functools import reduce
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv(), override=True)

root_path = os.getcwd()

filter_data = {}

def read_fileter():
    global filter_data
    f = ''
    f = os.getenv('FILTER_FILE')
    if f:
        path = os.getcwd() + '/'+ str(f) +'.yaml'
        if os.path.exists(path):
            with open(path, 'r') as f:
                filter_data = yaml.load(f.read(),Loader=yaml.FullLoader)


def filter_response(name, method, data):

    read_fileter()
    body = {}
    filter_key = {}
    method = str(method).lower()

    if not isinstance(data, dict):
        data = json.loads(data)

    if not filter_data:
        return data

    for i in filter_data['filter_requests']:
        if name == i['api'] and method == i['method']:
            filter_key = i

    if filter_key:
        if 'need' in filter_key and 'miss' in filter_key:
            raise ValueError('need 和 miss 不能同时存在')
        if 'need' in filter_key:
            for i in filter_key['need']:
                if '.' in i:
                    load = data
                    for j in i.split('.'):
                        try:
                            j = int(j)
                            load = load[j]
                        except Exception as e:
                            load = load[j]
                    body[i] = load
                else:
                    body[i] = data[i]
        elif 'miss' in filter_key:
            for i in filter_key['miss']:
                if '.' in i:
                    load = data
                    y = i.split('.')
                    for j in y[:-1]:
                        try:
                            j = int(j)
                            load = load[j]
                        except Exception as e:
                            load = load[j]
                    del load[i[-1]]
                else:
                    del data[i]
            body = data    
    else:
        body = data
    return body
    
def filter_header(data):
    read_fileter()

    headers = {}
    if not filter_data:
        for k, v in data:
            headers[k] = v
    else:
        filter_headers = [i.lower() for i in filter_data['filter_headers']]
        for k, v in data:
            if k.lower() in filter_headers:
                headers[k] = v
    return str(headers)