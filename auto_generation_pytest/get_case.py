# -*- coding: utf-8 -*- 
'''
@summary:   初始化CaseData实例，获取测试用例
@usage: 
            from auto_generation_pytest.get_case import CaseData
            CaseData().get_data('log')
''' 

import os
import json
import sys

class CaseData(object):

    def __init__(self, path=None):
        #读取用例文件数据
        if path:
            self.path = os.getcwd()+'/'
        else:
            self.path = os.getcwd()+'/data/'
        

    def get_data(self, data, name):
        with open(self.path+data, 'r') as f:
            data = json.load(f)
        item = data.copy()
        for i in name.split('_', 1):
            print(i)
            item = item[i]
        return item

