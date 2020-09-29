# coding=utf-8
import json
import os
from auto_generation_pytest.utlis import combination_requeset, comb_data
from auto_generation_pytest.template import *
from auto_generation_pytest.inhert import recursion_inherit


class Create(object):
    def __init__(self, name):
        self.path = os.path.dirname(__file__) + '/'
        self.path_data = name + '.json'
        self.pydatapath = './data/' + self.path_data
        self.pyfilepath = './testcase/test_' + name + '.py'
        self.last_content = ''
        self.class_data_all = {}
        self.content_base_import = content_base_import.format(name)
        self.data = self.load_josn(name)
        self.init_file()

    @staticmethod
    def add_file(path, is_init=False):
        try:
            if not os.path.exists(path):
                os.mkdir(path)
        except Exception as e:
            print('创建' + path + '目录失败' + str(e))
        if is_init:
            path += '__init__.py'
            try:
                if not os.path.exists(path):
                    fd = open(path, "w", encoding="utf-8")
                    fd.close()
            except Exception as e:
                print('创建' + path + '目录失败' + str(e))

    @staticmethod
    def load_josn(name):
        with open(name + '.json', 'r') as f:
            data = json.load(f)
        return data

    def init_file(self):
        self.add_file('./data/')
        self.add_file('./assert_fuction/', True)
        self.add_file('./testcase/', True)
        self.add_file('./hook/', True)

    def save_case(self):
        with open(self.pyfilepath, 'w') as f:
            f.writelines(self.last_content)
        with open('./testcase/conftest.py', 'w') as f:
            f.writelines('')
        with open(self.pydatapath, 'w') as f:
            f.writelines(json.dumps(self.class_data_all, indent=4, ensure_ascii=False))

    def run(self):
        for test_class, value in self.data.items():
            # 生成当前接口的测试类
            content = content_class
            # 初始化当前接口测试类的测试数据
            if test_class not in self.class_data_all:
                self.class_data_all[test_class] = {}

            assert (value['process'] != ''), '接口' + test_class + '没有配置process'
            change_num = 0

            # 按照process数量生成具体测试方法
            for test_function, process in value['process'].items():
                function_body = ''

                # 如果当前进程可以被跳过，则不再生成测试代码
                if 'skip' in process and bool(process['skip']):
                    continue

                # 判断当前方法是否存在继承数据，如果存在继承数据则需要在调用测试数据时指定调用的接口
                is_inherit = False

                # 按照进程中的case设置，生成测试用例数据
                self.class_data_all[test_class][test_function] = comb_data(process['case'])
                #print(self.class_data_all)
                # 组合测试函数

                function_name = str.lower(test_class + '_' + test_function)
                function_id = test_class + '_' + test_function
                function_data = function_name + '_data'
                content += content_data.format(self.path_data, function_id, function_data, process['story'],
                                               process['severity'],
                                               'Test' + test_class, 'test_' + function_name)

                # 当存在继承时，进行继承的数据组合
                if process['inherit'] is not None:
                    inherit_content_all = ''
                    for i in process['inherit']:
                        if test_class == i['api']:
                            print(test_class + '不能继承自己的接口返回')
                        inherit_info = '''		#获取{}继承的接口{}的值\n'''.format(function_id, i['api'] + '_' + i['process'])

                        inherit_content, inherit_data = recursion_inherit(self.data, i,
                                                                          self.class_data_all[test_class][test_function],
                                                                          function_id, function_id)
                        function_body += inherit_info + inherit_content
                        self.class_data_all[test_class][test_function] = inherit_data

                        b = 'test_' + str.lower(i['api'] + '_' + i['process'])

                        if 'skip' in self.data[i['api']]['process'][i['process']] and \
                                self.data[i['api']]['process'][i['process']]['skip'] is not None:
                            if not self.data[i['api']]['process'][i['process']]['skip']:
                                inherit_content_all += content_dependency.format('Test' + i['api'], b)

                    content += inherit_content_all

                # 组合fixture
                function = content_function.format(function_name, function_data)

                if 'fixture' in process:
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
                        content_case_function = content_case_function.format(
                            function_data + '[\'' + function_id + '\']', xx,
                            function_data + '[\'' + function_id + '\']')

                        content += content_case_function

                assert_info += combination_requeset(value, function_data)

                # 配置接口断言
                for i in process['assert']:
                    if content_response not in assert_info:
                        if 'response' in i['value']:
                            assert_info += content_response
                    assert_info += content_process_assert.format(i['value'], i['info'])
                if is_inherit and function_id not in content_case_function:
                    assert_info = assert_info.replace('@#$', '[\'' + function_id + '\']')
                else:
                    assert_info = assert_info.replace('@#$', '')
                assert_info = assert_info.replace('{', '##+##').replace('}', '##-##')

                content += str(assert_info)

                
            # 补充feature和class信息
           
            #print(test_class)
            #content = content.replace('\n','***&****')
            #print(content)
            content = str(content).format(value['feature'], test_class)
            content = content.replace('##+##', '{').replace('##-##', '}')
            
            self.last_content += content

        self.last_content = self.content_base_import + self.last_content
        
        self.save_case()




