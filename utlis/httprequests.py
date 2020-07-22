import os
import requests
import json
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv(), override=True)


class HttpRequest(object):

    def __init__(self):
        self.session = requests.session()
        self.header = {}
        self.timeout = 60
        self.url = os.environ.get('HOST')

    def get(self, api ,data):
        response = None
        try:
            response = self.session.get(self.url + api, params=data, headers=self.header, timeout=self.timeout)
            response.raise_for_status()
        except Exception as e:
            print("HTTP请求异常，异常信息：%s" % str(e))
        return response

    def post(self, api, data):

        response = None
        data = json.dumps(data)
        try:
            response = self.session.post(self.url + api, data=data, headers=self.header, timeout=self.timeout)
            response.raise_for_status()
        except Exception as e:
            print("HTTP请求异常，异常信息：%s" % str(e))
        return response

    def req(self, api, method, data, header, url=None):
        if url:
            self.url = url
        self.header = header
        r = getattr(self, method)(self.url + '/' + api, data)
        return r

