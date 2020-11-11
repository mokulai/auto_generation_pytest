# coding=utf-8
import json
import os
import sys
import pytest
import random
import string

from auto_generation_pytest.utlis import combination_requeset, comb_data
from auto_generation_pytest.template import *
from auto_generation_pytest.inhert import recursion_inherit
from utlis import add_file, init_py, load_josn, set_config
from tempfile import NamedTemporaryFile,TemporaryDirectory

class Create(object):
    def __init__(self, name):
        self.set_env()
        self.path = os.path.dirname(__file__) + '/'
        self.case = ''
        self.config = ''
        self.find_name(name)
        self.last_content = ''
        self.class_data_all = {}
        self.content_base_import = content_base_import
        self.init_file()
        self.req_type = 'http'


    @staticmethod    
    def save_function(path, data):
       if not os.path.exists(path):
            with open(path, 'w') as f:
                f.writelines(data)

    def set_env(self):
        path = os.getcwd()+'/.env'
        env = {}
        if os.path.exists(path):
            with open(path, "r") as f:
                for i in f:
                    if "=" in i:
                        key, value = i.split("=")
                        os.environ[key] = value.strip()

    def make_pytest_line(self, name):
        name_list = name.split('::')
        name = name_list[0]
        case = '::Test'+ name_list[1]
        try:
            if len(name_list) == 3:
                case += '::test_'+ name_list[1].lower() + '_' + name_list[2].lower()
        except:
            sys.exit(1)
        self.case = case
        return name_list[0]

    def find_name(self, name):
        path = name
        if '::' in name and '/' in name:
            name_list = name.split('/')
            name = name_list[-1]
            dirname = name_list[0]
            name = self.make_pytest_line(name)
            path = dirname + '/' + name
        elif '::' in name:
            self.make_pytest_line(name)
            name = name.split('::')[0]
            path = name
        elif '/' in name:
            path = name
            name = name.split('/')[-1]
        if 'json' in name:
            name = name.replace('.json','')
        self.path_data = name + '.json'
        self.pydatapath = './data/' + self.path_data
        self.pyfilepath = './testcase/test_' + name + '.py'
        if 'json' in path:
            ctx = load_josn(path)
            if 'Config' in ctx:
                self.config = sorted(ctx['Config'].items(),key = lambda x:len(x[0]),reverse=True)
                self.data = set_config(self.config, ctx['TestCase'])
            else:
                self.data = ctx
        else:
            print('没有发现json文件')


    def init_file(self):
        init_host = 'HOST=127.0.0.1\nGRPCOX=127.0.0.1:6969'
        add_file('./assert_function/')
        init_py('./assert_function/', '__init__')
        init_py('./assert_function/', 'assert_function')
        add_file('./hook/')
        init_py('./hook/', '__init__')
        init_py('./hook/', 'hook')
        if not os.path.exists('.env'):
            with open('.env', 'w') as f:
                f.writelines(init_host)

    def save_case(self):
        add_file('./data/')
        add_file('./testcase/')
        init_py('./testcase/', '__init__')
        init_py('./testcase/', 'conftest')
        with open(self.pyfilepath, 'w') as f:
            f.writelines(self.last_content)

        with open(self.pydatapath, 'w') as f:
            f.writelines(json.dumps(self.class_data_all, indent=4, ensure_ascii=False))

    def run(self):
        plan_list = ['-v','-s']
        init_py('./', 'conftest')
        with NamedTemporaryFile('w+t',suffix='.json',dir=os.getcwd()) as f:
            f.write(json.dumps(self.class_data_all, indent=4, ensure_ascii=False))
            f.seek(0)
            frist_name = 'CaseData().get_data(\'' + self.path_data + '\''
            last_name = 'CaseData(\'./\').get_data(\'' + f.name.split('/')[-1] + '\''
            self.last_content = self.last_content.replace(frist_name, last_name)
            
            with NamedTemporaryFile('w+t',suffix='.py',dir=os.getcwd()) as py:
                py.write(self.last_content)
                py.seek(0)
                name = py.name+self.case
                plan_list.append(name)
                pytest.main(plan_list)

    def make_pytest(self):
        self.req_type = 'http'
        for test_class, value in self.data.items():
            if value['method'] == 'grpc':
                self.req_type = 'grpc'
            # 生成当前接口的测试类
            content = content_class
            # 初始化当前接口测试类的测试数据
            if test_class not in self.class_data_all:
                self.class_data_all[test_class] = {}

            assert (value['process'] != ''), '接口' + test_class + '没有配置process'

            # 按照process数量生成具体测试方法
            for test_function, process in value['process'].items():
                if isinstance(process,str):
                    process = set_config(self.config, load_josn(process))
                elif 'path' in process and process['path'] is not None:
                    process.update(set_config(self.config, load_josn(process['path'])))
                    del process['path']

                function_body = ''
                if 'severity' not in process:
                    process['severity'] = 'p0'
                if 'inherit' not in process:
                    process['inherit'] = None
                # 如果当前进程可以被跳过，则不再生成测试代码
                if 'skip' in process and bool(process['skip']):
                    continue

                # 判断当前方法是否存在继承数据，如果存在继承数据则需要在调用测试数据时指定调用的接口
                is_inherit = False

                # 按照进程中的case设置，生成测试用例数据
                self.class_data_all[test_class][test_function] = comb_data(process['case'])

                # 组合测试函数
                function_name = str.lower(test_class + '_' + test_function)
                function_id = test_class + '_' + test_function
                function_data = function_name + '_data'
                content += content_data.format(self.path_data, function_id, function_data, process['story'],
                                               process['severity'],
                                               'Test' + test_class, 'test_' + function_name)

                # 当存在继承时，进行继承的数据组合
                if 'inherit' in process and process['inherit'] is not None:
                    inherit_content_all = ''
                    for i in process['inherit']:

                        inherit_info = '''		#获取{}继承的接口{}的值\n'''.format(function_id, i['api'] + '_' + i['process'])
                        inherit_content, inherit_data = recursion_inherit(self.data, i,
                                                                          self.class_data_all[test_class][test_function],
                                                                          function_id, function_id, self.config)
                        function_body += inherit_info + inherit_content
                        self.class_data_all[test_class][test_function] = inherit_data

                        b = 'test_' + str.lower(i['api'] + '_' + i['process'])

                        if 'skip' in self.data[i['api']]['process'][i['process']] and \
                                self.data[i['api']]['process'][i['process']]['skip'] is not None:
                            if not self.data[i['api']]['process'][i['process']]['skip']:
                                dependency = content_dependency.format('Test' + i['api'], b)
                                if dependency not in inherit_content_all:
                                    inherit_content_all += dependency

                    content += inherit_content_all

                # 组合fixture
                function = content_function.format(function_name, function_data)

                if 'fixture' in process and process['fixture'] is not None:
                    fixture_index = function.index('self') + 4
                    function = function[:fixture_index] + ',{}' + function[fixture_index:]
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
                        if process['inherit'] is not None:
                            content_case_function = content_case_function.format(
                                function_data + '[\'' + function_id + '\']', xx,
                                function_data + '[\'' + function_id + '\']')
                            assert_info += '''		{} = {}\n'''.format('req', function_data + '[\'' + function_id + '\']')
                        else:
                            content_case_function = content_case_function.format(function_data, xx, function_data)
                            assert_info += '''		{} = {}\n'''.format('req', function_data)
                        content += content_case_function
                else:
                    content += '''		{} = {}\n'''.format('req', function_data)
                assert_info += combination_requeset(value, function_data)

                # 配置接口断言
                for i in process['assert']:
                    assert_info += content_process_assert.format(i['value'], i['info']) + "+str(r)\n"
                if is_inherit and function_id not in content_case_function:
                    assert_info = assert_info.replace('@#$', '[\'' + function_id + '\']')
                else:
                    assert_info = assert_info.replace('@#$', '')
                assert_info = assert_info.replace('{', '##+##').replace('}', '##-##')

                content += str(assert_info)

            # 补充feature和class信息
            content = str(content).format(value['feature'], test_class)
            content = content.replace('##+##', '{').replace('##-##', '}')

            self.last_content += content
        
        # 组合pytest代码
        if self.req_type == 'grpc':
            req = grpc_import
        elif self.req_type == 'http':
            req = http_import
        data = self.last_content
        if os.path.exists(self.pyfilepath):
            with open(self.pyfilepath, 'r') as f:
                old = str(f.read())
                head = old[:old.index('@allure.feature')-1]
            data = head + self.last_content
        else:
            data = self.content_base_import + req +self.last_content
        self.last_content = data.replace('\t','    ')
        
        return self