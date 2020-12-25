# coding=utf-8
import io
import os
import sys
import unittest
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
sys.path.append(curPath)
from auto_generation_pytest.cli import main

class TestCli(unittest.TestCase):
    def test_show_version(self):
        #sys.argv = ["mat", "run", "demo/demo_http::Detail::Case1"]
        #sys.argv = ["mat", "run", "demo/demo_http::Detail"]
        #sys.argv = ["mat", "run", "demo/demo_http"]
        #sys.argv = ["mat", "run", "demo_grpc"]
        #sys.argv = ["mat", "init"]
        #sys.argv = ["mat", "create", "demo/demo_http"]
        #sys.argv = ["mat", "proxy"]
        sys.argv = ["mat", "create", "pms/pms_record.json"]
        with self.assertRaises(SystemExit) as cm:
            main()
        #self.assertEqual(cm.exception.code, 0)

if __name__ == "__main__":
  unittest.main()