# coding=utf-8
import json
import os
from utlis.utlis import combination_requeset, comb_data
from utlis.template import *
from utlis.inhert import recursion_inherit

api_name = 'demo'

with open(api_name+'.json', 'r') as f:
    data = json.load(f)

path = os.path.dirname(__file__) + '/'
path_data = api_name+'.json'
pydatapath = './data/' + path_data
pyfilepath = './testcase/test_' + api_name + '.py'

try:
    os.mkdir(path)
except Exception as e:
    pass
try:
    os.mkdir('./data/')
except Exception as e:
    pass
try:
    os.mkdir('./assert_fuction/')
    fd = open('./assert_fuction/__init__.py', "w", encoding="utf-8")
    fd.close()
except Exception as e:
    pass
try:
    os.mkdir('./hook/')
    fd = open('./hook/__init__.py', "w", encoding="utf-8")
    fd.close()
except Exception as e:
    pass

last_content = ''
class_data_all = {}

content_base_import = content_base_import.format(api_name)

for test_class, value in data.items():
    # 生成当前接口的测试类
    content = content_class
    # 初始化当前接口测试类的测试数据
    if test_class not in class_data_all:
        class_data_all[test_class] = {}

    assert (value['process'] != ''), '接口' + test_class + '没有配置process'
    change_num = 0

    # 按照process数量生成具体测试方法
    for test_function, process in value['process'].items():
        function_body = ''
        content_function_change = ''
        # 如果当前进程可以被跳过，则不再生成测试代码
        if 'skip' in process and bool(process['skip']):
            continue

        # 判断当前方法是否存在继承数据，如果存在继承数据则需要在调用测试数据时指定调用的接口
        is_inherit = False

        # 按照进程中的case设置，生成测试用例数据
        class_data_all[test_class][test_function] = comb_data(process['case'])
        # 组合测试函数

        function_name = str.lower(test_class + '_' + test_function)
        function_id = test_class + '_' + test_function
        function_data = function_name + '_data'
        content += content_data.format(path_data, function_id, function_data, process['story'], process['severity'],
                                       'Test' + test_class, 'test_' + function_name)

        # 当存在继承时，进行继承的数据组合
        if process['inherit'] is not None:
            inherit_content_all = ''
            for i in process['inherit']:
                if test_class == i['api']:
                    print(test_class + '不能继承自己的接口返回')
                inherit_info = '''		#获取{}继承的接口{}的值\n'''.format(function_id, i['api'] + '_' + i['process'])

                inherit_content, inherit_data = recursion_inherit(data, i, class_data_all[test_class][test_function],
                                                                  function_id, function_id)
                function_body += inherit_info + inherit_content
                class_data_all[test_class][test_function] = inherit_data

                b = 'test_' + str.lower(i['api'] + '_' + i['process'])

                if 'skip' in data[i['api']]['process'][i['process']] and data[i['api']]['process'][i['process']]['skip'] is not None:
                    if not data[i['api']]['process'][i['process']]['skip']:
                        inherit_content_all += content_dependency.format('Test' + i['api'], b)

            content += inherit_content_all

        # 组合fixture
        function = content_function.format(function_name, function_data)

        if 'fixture' in process:
            fixture_index = function.index('self')+4
            function = function[:fixture_index]+',{}'+function[fixture_index:]
            fixture = ','.join(process['fixture'])
            function = function.format(fixture)
            fixture = ','.join(process['fixture'])
        content += function
        content += function_body


        content_case_function = ''
        assert_info = '''		#开始进行被测接口的测试\n'''
        if 'hooks' in process and process['hooks'] is not None:

            content += '''		#对待测数据进行处理\n'''
            for xx in process['hooks']:

                content_case_function = '''		{} = {}({})\n'''
                content_case_function = content_case_function.format(function_data+'[\''+function_id+'\']', xx, function_data+'[\''+function_id+'\']')

                content += content_case_function
        assert_info += combination_requeset(value, function_data)

        # 配置接口断言
        for i in process['assert']:
            if content_respone not in assert_info:
                if 'respone' in i['value']:
                    assert_info += content_respone
            assert_info += content_process_assert.format(i['value'], i['info'])
        if is_inherit and function_id not in content_case_function:
            assert_info = assert_info.replace('@#$', '[\'' + function_id + '\']')
        else:
            assert_info = assert_info.replace('@#$', '')
        content += str(assert_info)

    # 补充feature和class信息
    content = str(content).format(value['feature'], test_class)
    content = content.replace('##+##', '{').replace('##-##', '}')

    last_content += content


last_content = content_base_import + last_content


with open(pyfilepath, 'w') as f:
    f.writelines(last_content)

with open(pydatapath, 'w') as f:
    f.writelines(json.dumps(class_data_all, indent=4, ensure_ascii=False))


