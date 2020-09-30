import os
import requests
import json
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv(), override=True)

class BaseRpc(object):

    def __init__(self, host, path):
        self.host = host
        self.url = os.environ.get('GRPCOX')
        url = self.url + "/server/"+self.host+"/services"
        proto_list = self.find_proto(path)
        querystring = {"restart":"0"}
        r = requests.request("POST", url, files=proto_list, params=querystring)
        assert(r.status_code==200),"grpc服务链接错误"

    def find_proto(self, path):
        list_file = os.listdir(path)
        proto_list = []
        for file_name in list_file:
            if file_name.endswith('.proto'):
                proto_file = ('protos', (file_name,open(path+'/'+file_name,'rb')))
                proto_list.append(proto_file)
        return proto_list

    def send(self, services, request, message):
        headers = {
            'Content-Type': "application/json"
        }
        url = self.url + "/server/"+self.host+"/function/"+services+"."+request+"/invoke"
        message = json.dumps(message)
        response = requests.request("POST", url, data=message, headers=headers)
        data = response.json()
        return data['data']['result']