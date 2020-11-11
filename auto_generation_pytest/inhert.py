
from auto_generation_pytest.template import content_process_assert
from auto_generation_pytest.combination.combination_inhert import singel_case_and_singel_inhert, all_case_and_singel_inhert, all_case_and_loop_inhert, singel_case_and_loop_inhert
from auto_generation_pytest.utlis import comb_data, combination_requeset
from dotenv import find_dotenv, load_dotenv
from utlis import load_josn, set_config
load_dotenv(find_dotenv(), override=True)

is_inheri = False

def recursion_inherit(data, case, base, name, data_name=None, c=None):
    test_function, test_class = name.split('_')
    function_data = str.lower(name) + '_data'
    global is_inherit
    if data[case['api']] is not None:
        content = ''
        inherit_data = {}
        inherit = data[case['api']]
        inherit_process_name = case['api'] + '_' + case['process']
        if inherit_process_name in base[0]:
            num = list(base[0].keys()).count(inherit_process_name)
            inherit_process_name += str(num)
        by_inherit = inherit['process'][case['process']]
        if isinstance(by_inherit,str):
            by_inherit = set_config(c,load_josn(by_inherit))
        elif 'path' in by_inherit and by_inherit['path'] is not None:
            by_inherit.update(set_config(c, load_josn(by_inherit['path'])))
            del by_inherit['path']
        if inherit['process'] == "":
            print('inherit process不可为空')
        else:

            assert (case['api'] + case[
                'process'] != test_class + test_function), test_class + '接口的' + test_function + '不能继承自己的流程'

            if 'hooks' in by_inherit and by_inherit['hooks'] is not None:

                for xx in by_inherit['hooks']:

                    content_case_function = '''		{} = {}({}['{}'])\n'''
                    content_case_function = content_case_function.format(function_data+'[\''+inherit_process_name +'\']',xx, function_data, inherit_process_name)

                    content += content_case_function

            if case['case'] is None:

                # 如果有流程，而且没给出具体要的数据，说明是完全依赖上一个接口返回的数据的，需要获取依赖接口的全部数据，作为用例数据

                value = comb_data(by_inherit['case'])
                         
                if data_name is not None and data_name == name:
                    inherit_data = all_case_and_singel_inhert(inherit_process_name, value, name, base)
                else:
                    inherit_data = all_case_and_loop_inhert(inherit_process_name, value, base)

                content += combination_requeset(data[case['api']], function_data+'[\''+ inherit_process_name + '\']')
                is_inherit = True

            else:
                if data_name is not None and data_name == name:
                    inherit_data = singel_case_and_singel_inhert(inherit_process_name, case['case'], name, base)
                else:
                    inherit_data = singel_case_and_loop_inhert(inherit_process_name, case['case'], base)
                content += combination_requeset(data[case['api']], function_data+'[\''+ inherit_process_name + '\']')

                is_inherit = True


            # 如果有skip说明该集成对process不再单独执行，需要在此保证该测例运行正确
            if 'skip' in by_inherit and bool(by_inherit):
                for i in by_inherit['assert']:
                    i['value'] = i['value'].replace('{', '##+##').replace('}', '##-##')
                    content += content_process_assert.format(i['value'], i['info'])+ "+str(r)\n"

            # 继承接口需要指定的值
            if case['data'] is not  None:
                for need_inherit_key, need_inherit_value in case['data'].items():
                    inherit_value_list = need_inherit_value.split('.')
                    check_api_name = inherit_value_list[0]
                    load = ''
                    for x in inherit_value_list[1:]:
                        try:
                            x = int(x)
                            load += '[{}]'.format(x)
                        except Exception :
                            load += '[\'{}\']'.format(x)

                    assert (check_api_name == case['api']), '需要继承的接口和取值的接口名称不同'
                    content += '''\t\t{}['{}']['{}'] = r{} \n'''.format(function_data, name, need_inherit_key, load)

            for process_key, process_value in inherit['process'].items():
                if isinstance(process_value,str):
                    process_value = set_config(c,load_josn(process_value))
                elif 'path' in process_value and process_value['path'] is not None:
                    process_value.update(set_config(c, load_josn(process_value['path'])))
                    del process_value['path']
                if process_value['inherit'] is not None and process_key == case['process']:
                    for i in process_value['inherit']:
                        assert (name != i['api']), name + '接口和' + case['api'] + '接口死锁'
                        b = '''		#获取{}继承的接口{}的值\n'''.format(case['api'], i['api'] )
                        inherit_content, inherit_data = recursion_inherit(data, i, inherit_data, name, c)
                        content = b + inherit_content + content

    return content, inherit_data