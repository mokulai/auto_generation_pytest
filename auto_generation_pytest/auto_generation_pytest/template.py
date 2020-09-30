
content_base_import = '''# -*- coding: utf-8 -*- 
import allure
import grpc
import pytest
import pytest_dependency

from auto_generation_pytest.get_case import CaseData
from assert_fuction import *
from hook import *
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

content_process_assert = '''		assert({}), u"{}"
'''
