from mitmproxy import proxy, options
from mitmproxy.tools.dump import DumpMaster
from mitmproxy.script import concurrent
from mitmproxy import flowfilter
from mitmproxy import ctx, http
import time
import json
import os
import signal
import time
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
sys.path.append(curPath)

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv(), override=True)

from save import save_case
from res_filter import filter_header,filter_response

from auto_generation_pytest.utlis import find_num, add_file, init_py

HOST = ''
NAME = ''
PORT = 0
num = 0

class Catch(object):

    def __init__(self):
        def handler(signum, frame):
            os.system('networksetup -setwebproxystate "Wi-Fi" off')
            os.system('networksetup -setsecurewebproxystate "Wi-Fi" off')
            sys.exit(0)
        signal.signal(signal.SIGINT, handler)
        os.system('networksetup -setwebproxy "Wi-Fi" 0.0.0.0 ' + str(PORT))
        os.system('networksetup -setsecurewebproxy "Wi-Fi" 0.0.0.0 ' + str(PORT))
        init_host = 'HOST=' + os.getenv('HOST') + '\nHTTP_FROMAT=json'
        path = './'+NAME+'/'
        add_file(path)
        add_file(path+'data/')
        init_py(path, 'conftest')
        with open(path+'.env', 'w') as f:
            f.writelines(init_host)

    @staticmethod
    def response(flow):
        global num

        # 保留指定地址的接口请求
        if HOST not in flow.request.pretty_url:
            return
        if '.js' in flow.request.pretty_url:
            return
        if '.css' in flow.request.pretty_url:
            return
        # 保留返回格式为json的数据
        if 'Content-Type' not in flow.response.headers:
            return
        if 'application/json' not in flow.response.headers['Content-Type']:
            return

        # 保留状态码为200的数据
        if flow.response.status_code != 200:
            return

        body = {}
        process = {}

        # 获取api名称
        if ':' in flow.request.pretty_url.replace('://',''):
            url = '/' + '/'.join(flow.request.pretty_url.split(':')[2].split('/')[1:])
        else:
            url = flow.request.pretty_url.split('?')[0].replace(HOST, '')

        # 根据请求方式处理请求参数
        
        method = str.lower(flow.request.method)
        
        if flow.request.method == 'GET':
            if '?' in url:
                url = url.split('?')[0]
            body = dict(flow.request.query.fields)
        else:
            if flow.request.text:
                body = json.loads(flow.request.text)

        name = str.upper(flow.request.method) + ''.join([i.capitalize() for i in url.split('/')])

        # 仅保留需要的信息
        headers = filter_header(flow.request.headers.items())
        response = filter_response(url, flow.request.method, flow.response.text)

        if num != 0:
            num += 1

        else:
            num = find_num(NAME)

        data = {
            "record_name": NAME,
            "index": num,
            "case_name": name,
            "api": url,
            "method": method,
            "head": headers,
            "body": body,
            "response": response
        }
        save_case(data)


def start():
    global HOST
    global NAME
    global PORT
    HOST = os.getenv('PROXY_HOST')
    NAME = os.getenv('RECORD_NAME')
    PORT = int(os.getenv('PROXY_PORT'))
    myaddon = Catch()
    opts = options.Options(listen_port=PORT)
    pconf = proxy.config.ProxyConfig(opts)
    m = DumpMaster(opts)
    m.server = proxy.server.ProxyServer(pconf)
    m.addons.add(myaddon)
    try:
        m.run()
    except KeyboardInterrupt:
        m.shutdown()
