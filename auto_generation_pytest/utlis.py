from auto_generation_pytest.combination.combination_case import Comb
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]

def grpc_request_format(d, case):
    req = '''\t\treq = BaseRpc(\'{}\', \'{}\')\n\t\tr = req.send(\'{}\',\'{}\',{})\n'''.format(d['url'], rootPath+d['proto'], d['server'], d['request'], case)
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
        elif i['data'] and comb_method:
            output.append(i['data'])
    if output == ['']:
        output = [{}]
    return output

