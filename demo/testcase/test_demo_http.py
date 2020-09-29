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


@allure.feature(u'demo接口1')
class TestTestDetail(object):
	
	@pytest.fixture(params=CaseData().get_data('demo_http.json','TestDetail_TestCase1'))
	def testdetail_testcase1_data(self, request):
		return request.param

	@allure.story(u'demo测试')
	@allure.severity('p0')
	@pytest.mark.dependency(name="TestTestDetail::test_testdetail_testcase1")
	@pytest.mark.dependency(depends=["TestTestApi::test_testapi_case"]) 
	def test_testdetail_testcase1(self,cookie,testdetail_testcase1_data):
		#获取TestDetail_TestCase1继承的接口TestApi_Case的值
		testdetail_testcase1_data['TestApi_Case'] = transform(testdetail_testcase1_data['TestApi_Case'])
		r = HttpRequest().send('/api/test-api1', 'get', testdetail_testcase1_data['TestApi_Case'], {'Content-Type': 'application/json'})
		assert(r.status_code == 200), u"接口调用失败"
		respone = r.json()
		testdetail_testcase1_data['TestDetail_TestCase1']['demo_3'] = respone[1]['demo'] 
		#对待测数据进行处理
		testdetail_testcase1_data['TestDetail_TestCase1'] = transform(testdetail_testcase1_data['TestDetail_TestCase1'])
		#开始进行被测接口的测试
		r = HttpRequest().send('/api/test-detail', 'post', testdetail_testcase1_data, {'Content-Type': 'application/json'})
		respone = r.json()
		assert(assert_check(response)), u"接口调用失败"
	
	@pytest.fixture(params=CaseData().get_data('demo_http.json','TestDetail_TestCase2'))
	def testdetail_testcase2_data(self, request):
		return request.param

	@allure.story(u'demo测试')
	@allure.severity('p0')
	@pytest.mark.dependency(name="TestTestDetail::test_testdetail_testcase2")
	@pytest.mark.dependency(depends=["TestTestApi2::test_testapi2_case"]) 
	def test_testdetail_testcase2(self,cookie,testdetail_testcase2_data):
		#获取TestDetail_TestCase2继承的接口TestApi2_Case的值
		#获取TestApi2继承的接口TestApi的值
		testdetail_testcase2_data['TestApi_Case'] = transform(testdetail_testcase2_data['TestApi_Case'])
		r = HttpRequest().send('/api/test-api1', 'get', testdetail_testcase2_data['TestApi_Case'], {'Content-Type': 'application/json'})
		assert(r.status_code == 200), u"接口调用失败"
		respone = r.json()
		testdetail_testcase2_data['TestDetail_TestCase2']['demo_3'] = respone[0]['demo'] 
		r = HttpRequest().send('/api/test-api2', 'get', testdetail_testcase2_data['TestApi2_Case'], {'Content-Type': 'application/json'})
		assert(r.status_code == 200), u"接口调用失败"
		respone = r.json()
		testdetail_testcase2_data['TestDetail_TestCase2']['demo_3'] = respone[1]['demo'] 
		#对待测数据进行处理
		testdetail_testcase2_data['TestDetail_TestCase2'] = transform(testdetail_testcase2_data['TestDetail_TestCase2'])
		#开始进行被测接口的测试
		r = HttpRequest().send('/api/test-detail', 'post', testdetail_testcase2_data, {'Content-Type': 'application/json'})
		assert(r.status_code == 200), u"接口调用失败"
	
	@pytest.fixture(params=CaseData().get_data('demo_http.json','TestDetail_TestCase3'))
	def testdetail_testcase3_data(self, request):
		return request.param

	@allure.story(u'demo测试')
	@allure.severity('p0')
	@pytest.mark.dependency(name="TestTestDetail::test_testdetail_testcase3")
	@pytest.mark.dependency(depends=["TestTestApi::test_testapi_case"]) 
	@pytest.mark.dependency(depends=["TestTestApi3::test_testapi3_case"]) 
	def test_testdetail_testcase3(self,cookie,testdetail_testcase3_data):
		#获取TestDetail_TestCase3继承的接口TestApi_Case的值
		testdetail_testcase3_data['TestApi_Case'] = transform(testdetail_testcase3_data['TestApi_Case'])
		r = HttpRequest().send('/api/test-api1', 'get', testdetail_testcase3_data['TestApi_Case'], {'Content-Type': 'application/json'})
		assert(r.status_code == 200), u"接口调用失败"
		respone = r.json()
		testdetail_testcase3_data['TestDetail_TestCase3']['demo_3'] = respone[1]['demo'] 
		#获取TestDetail_TestCase3继承的接口TestApi3_Case的值
		r = HttpRequest().send('/api/test-api3', 'get', testdetail_testcase3_data['TestApi3_Case'], {'Content-Type': 'application/json'})
		assert(r.status_code == 200), u"接口调用失败"
		respone = r.json()
		testdetail_testcase3_data['TestDetail_TestCase3']['demo_3'] = respone[1]['demo'] 
		#对待测数据进行处理
		testdetail_testcase3_data['TestDetail_TestCase3'] = transform(testdetail_testcase3_data['TestDetail_TestCase3'])
		#开始进行被测接口的测试
		r = HttpRequest().send('/api/test-detail', 'post', testdetail_testcase3_data, {'Content-Type': 'application/json'})
		assert(r.status_code == 200), u"接口调用失败"

@allure.feature(u'demo接口')
class TestTestApi(object):
	
	@pytest.fixture(params=CaseData().get_data('demo_http.json','TestApi_Case'))
	def testapi_case_data(self, request):
		return request.param

	@allure.story(u'demo测试')
	@allure.severity('p0')
	@pytest.mark.dependency(name="TestTestApi::test_testapi_case")
	def test_testapi_case(self,cookie,testapi_case_data):
		#对待测数据进行处理
		testapi_case_data['TestApi_Case'] = transform(testapi_case_data['TestApi_Case'])
		#开始进行被测接口的测试
		r = HttpRequest().send('/api/test-api1', 'get', testapi_case_data, {'Content-Type': 'application/json'})
		assert(r.status_code == 200), u"接口调用失败"

@allure.feature(u'demo接口')
class TestTestApi2(object):
	
	@pytest.fixture(params=CaseData().get_data('demo_http.json','TestApi2_Case'))
	def testapi2_case_data(self, request):
		return request.param

	@allure.story(u'demo测试')
	@allure.severity('p0')
	@pytest.mark.dependency(name="TestTestApi2::test_testapi2_case")
	@pytest.mark.dependency(depends=["TestTestApi::test_testapi_case"]) 
	def test_testapi2_case(self,cookie,testapi2_case_data):
		#获取TestApi2_Case继承的接口TestApi_Case的值
		testapi2_case_data['TestApi_Case'] = transform(testapi2_case_data['TestApi_Case'])
		r = HttpRequest().send('/api/test-api1', 'get', testapi2_case_data['TestApi_Case'], {'Content-Type': 'application/json'})
		assert(r.status_code == 200), u"接口调用失败"
		respone = r.json()
		testapi2_case_data['TestApi2_Case']['demo_3'] = respone[0]['demo'] 
		#开始进行被测接口的测试
		r = HttpRequest().send('/api/test-api2', 'get', testapi2_case_data, {'Content-Type': 'application/json'})
		assert(r.status_code == 200), u"接口调用失败"

@allure.feature(u'demo接口')
class TestTestApi3(object):
	
	@pytest.fixture(params=CaseData().get_data('demo_http.json','TestApi3_Case'))
	def testapi3_case_data(self, request):
		return request.param

	@allure.story(u'demo测试')
	@allure.severity('p0')
	@pytest.mark.dependency(name="TestTestApi3::test_testapi3_case")
	def test_testapi3_case(self,cookie,testapi3_case_data):
		#开始进行被测接口的测试
		r = HttpRequest().send('/api/test-api3', 'get', testapi3_case_data, {'Content-Type': 'application/json'})
		assert(r.status_code == 200), u"接口调用失败"
