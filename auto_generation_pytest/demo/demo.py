# coding=utf-8
import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
sys.path.append(curPath)

from auto_generation_pytest.create import Create

c = Create('demo_grpc')
c.run()
c = Create('demo_http')
c.run()