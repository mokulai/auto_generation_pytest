# -*- coding: utf-8 -*- 
import requests
import csv
import time 
import json
import allure
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


@allure.feature(u'uac模块 grpc 测试')
class TestTestUac(object):
	
	@pytest.fixture(params=CaseData().get_data('demo_grpc.json','TestUac_TestCase'))
	def testuac_testcase_data(self, request):
		return request.param

	@allure.story(u'uac测试')
	@allure.severity('p0')
	@pytest.mark.dependency(name="TestTestUac::test_testuac_testcase")
	@pytest.mark.dependency(depends=["TestTestHello::test_testhello_testcase"]) 
	@pytest.mark.dependency(depends=["TestTestHello::test_testhello_testcase"]) 
	def test_testuac_testcase(self,cookie,testuac_testcase_data):
		#获取TestUac_TestCase继承的接口TestHello_TestCase的值
		testuac_testcase_data['TestHello_TestCase'] = transform(testuac_testcase_data['TestHello_TestCase'])
		req = BaseRpc('ip:50052', '/Users/jieshi/Desktop/mat/JKKJ/pb2/hello')
		r = req.send('hello.Greeter','SayHello',testuac_testcase_data['TestHello_TestCase'])
		assert(r.strip() == '{"message": "Hello, 1!"}'), u"返回错误"
		respone = r.json()
		testuac_testcase_data['TestUac_TestCase']['demo_3'] = respone[1]['demo'] 
		#获取TestUac_TestCase继承的接口TestHello_TestCase的值
		testuac_testcase_data['TestHello_TestCase1'] = transform(testuac_testcase_data['TestHello_TestCase1'])
		req = BaseRpc('ip:50052', '/Users/jieshi/Desktop/mat/JKKJ/pb2/hello')
		r = req.send('hello.Greeter','SayHello',testuac_testcase_data['TestHello_TestCase1'])
		assert(r.strip() == '{"message": "Hello, 1!"}'), u"返回错误"
		respone = r.json()
		testuac_testcase_data['TestUac_TestCase']['demo_3'] = respone[2]['demo'] 
		#对待测数据进行处理
		testuac_testcase_data['TestUac_TestCase'] = transform(testuac_testcase_data['TestUac_TestCase'])
		#开始进行被测接口的测试
		req = BaseRpc('uac', '/Users/jieshi/Desktop/mat/JKKJ/pb2/uac')
		r = req.send('app.UacApiRpc','RegisterByYiYe',testuac_testcase_data)
		assert(r.strip() == '{ "message": "Hello, 1!"}'), u"返回错误"

@allure.feature(u'hello模块 grpc 测试')
class TestTestHello(object):
	
	@pytest.fixture(params=CaseData().get_data('demo_grpc.json','TestHello_TestCase'))
	def testhello_testcase_data(self, request):
		return request.param

	@allure.story(u'hello测试')
	@allure.severity('p0')
	@pytest.mark.dependency(name="TestTestHello::test_testhello_testcase")
	def test_testhello_testcase(self,cookie,testhello_testcase_data):
		#对待测数据进行处理
		testhello_testcase_data['TestHello_TestCase'] = transform(testhello_testcase_data['TestHello_TestCase'])
		#开始进行被测接口的测试
		req = BaseRpc('ip:50052', '/Users/jieshi/Desktop/mat/JKKJ/pb2/hello')
		r = req.send('hello.Greeter','SayHello',testhello_testcase_data)
		assert(r.strip() == '{"message": "Hello, 1!"}'), u"返回错误"
