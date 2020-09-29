
content_base_import = '''# -*- coding: utf-8 -*- 
import requests
import csv
import time 
import json
import allure
import grpc
import pytest
import pytest_dependency
import sys
import os
#添加当前工程目录
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
#添加当前文件目录
sys.path.append(os.path.dirname(__file__))

from auto_generation_pytest.httprequests import HttpRequest
from auto_generation_pytest.get_case import *
from assert_fuction import *
from hook import *

'''

content_class = '''
@allure.feature(u'{}')
class Test{}(object):
'''

content_dependency = '''	@pytest.mark.dependency(depends=["{}::{}"]) 
'''

content_data = '''	
	@pytest.fixture(params=CaseData().get_data('{}','{}'))
	def {}(self, request):
		return request.param

	@allure.story(u'{}')
	@allure.severity('{}')
	@pytest.mark.dependency(name="{}::{}")
'''

content_function = '''	def test_{}(self,{}):\n'''

content_response = '''		respone = r.json()\n'''

content_process_assert = '''		assert({}), u"{}"
'''
