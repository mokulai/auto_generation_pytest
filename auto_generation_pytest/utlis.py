from auto_generation_pytest.combination.combination_case import Comb
import os
import json
import random
import string

def grpc_request_format(d, case):
    req = '''\t\trpc = BaseRpc(\'{}\', \'{}\')\n\t\tr = rpc.send(\'{}\',\'{}\',{})\n'''.format(d['url'], d['proto'], d['server'], d['request'], case)
    return req.replace('{', '##+##').replace('}', '##-##')

def http_request_format(d, case):
    if 'url' in d and d['url'] != '':
        req = '''\t\tr = HttpRequest().send(\'{}\', \'{}\', {}, {}, url=\'{}\')\n'''.format(
            d['api'], d['method'], case, d['head'], d['url'])
    else:
        req = '''\t\tr = HttpRequest().send(\'{}\', \'{}\', {}, {})\n'''.format(
            d['api'], d['method'], case, d['head'])
    return req.replace('{', '##+##').replace('}', '##-##')

def combination_requeset(d, case):
    if d['method'] == 'grpc':
        return grpc_request_format(d, case)
    else:
        return http_request_format(d, case)

def comb_data(data):
    output = []
    for temporary in data:
        i = temporary.copy()
        # 获取当前数据的组合方式
        comb_method = i.pop('comb')
        # 根据变量的组合方式，进行变量组合
        comb = Comb(i)
        if comb_method in ['allpairs', 'multiply', 'normal']:
            i['var'] = getattr(comb, comb_method)()
            output += comb.fusion(i)
        elif comb_method in ['random']:
            output += comb.random()
        elif i['data']:
            output.append(i['data'])
    if output == ['']:
        output = [{}]
    return output

def add_file(path):
    try:
        if not os.path.exists(path):
            os.mkdir(path)
    except Exception as e:
        print('创建' + path + '目录失败' + str(e))

def init_py(path, pyname):
    path += pyname + '.py'
    try:
        if not os.path.exists(path):
            fd = open(path, "w", encoding="utf-8")
            fd.close()
    except Exception as e:
        print('创建' + path + ' ' +pyname + '失败' + str(e))

def load_josn(name):
    with open(name, 'r') as f:
        data = json.load(f)
    return data

def set_config(config, data):
    if config == '':
        return data
    data = json.dumps(data)
    for key, value in config:
        name = '$' + key
        if 'env(' in value:
            value = value.replace('env(','').replace(')','').strip('\'').strip('"')
            value = os.getenv(value)
        if isinstance(value,str):
            data = data.replace(name,str(value))
        else:
            random_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
            value = random_str + str(value).replace('\'','"') +random_str
            data = data.replace(name,str(value))
            data = data.replace('"'+random_str,'').replace(random_str+'"','')
    data = json.loads(data)
    return data