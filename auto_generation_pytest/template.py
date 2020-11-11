
content_base_import = '''# -*- coding: utf-8 -*- 
import allure
import grpc
import pytest
import pytest_dependency
import os
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv(), override=True)

from auto_generation_pytest.get_case import CaseData
from assert_function.assert_function import *
from hook.hook import *


'''

grpc_import = '''from auto_generation_pytest.grpcrequests import BaseRpc
'''

http_import = '''from auto_generation_pytest.httprequests import HttpRequest
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

content_process_assert = '''		assert({}), u"{}'''

base = ''' # coding=utf-8
import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
sys.path.append(curPath)
'''

function_item = ''' 
def {}():
	pass'''
