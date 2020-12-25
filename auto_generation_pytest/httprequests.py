import os
import requests
import json
import importlib
from dotenv import find_dotenv, load_dotenv
from auto_generation_pytest.utlis import get_extract,set_extract
load_dotenv(find_dotenv(), override=True)


class HttpRequest(object):

    def __init__(self):
        self.session = requests.session()
        self.session.keep_alive = False
        self.header = {}
        self.timeout = 60
        self.url = os.environ.get('HOST')
        self.format = str(os.environ.get('HTTP_FROMAT'))

    def res_format(self, data):
        path = self.format.split('.')
        funciton = importlib.import_module('.'.join(path[:-1]))
        response = getattr(funciton, path[-1])(data)
        return response

    def get(self, api ,data):
        response = None
        try:
            response = self.session.get(api, params=data, headers=self.header, timeout=self.timeout)
            response.raise_for_status()
        except Exception as e:
            print("HTTP请求异常，异常信息：%s \n" % str(e))
        if self.format == 'json':
            response = response.json()
        elif '.' in self.format:
            response = self.res_format(response)
        return response

    def post(self, api, data):
        response = None
        data = json.dumps(data)
        try:
            response = self.session.post(api, data=data, headers=self.header, timeout=self.timeout)
            response.raise_for_status()
        except Exception as e:
            print("HTTP请求异常，异常信息：%s \n" % str(e))
        if self.format == 'json':
            try:
                response = response.json()
            except Exception as e :
                print("返回结果格式化失败：%s \n" % str(response.text))
        elif '.' in self.format:
            try:
                response = self.res_format(response)
            except Exception as e :
                print("返回结果格式化失败：%s \n" % str(response.text))
        return response

    def send(self, api, method, data, header, url=None):
        if url:
            self.url = url
        self.header = header
        for k,v in data.items():
            if '$' in str(v):
                data[k] = get_extract(v.replace('$',''))
        method = str.lower(method)
        if not self.url:
            raise ValueError('未配置环境变量HOST')
        r = getattr(self, method)(self.url + api, data)
        return r

    
