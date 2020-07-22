# -*- coding: utf-8 -*- 
'''
@summary:   初始化CaseData实例，获取测试用例
@usage: 
            from utlis.get_case import CaseData
            CaseData().get_data('log')
''' 

import os
import json
import sys
sys.path.append('../')
class CaseData(object):

    def __init__(self):
        #读取用例文件数据
        self.path = os.path.dirname(os.path.dirname(__file__))+'/data/'

    def get_data(self, data, name):
        with open(self.path+data, 'r') as f:
            data = json.load(f)
        item = data.copy()
        for i in name.split('_', 1):
            print(i)
            item = item[i]
        return item

#print(CaseData().get_data('demo.json','TestDetail_TestCase1'))