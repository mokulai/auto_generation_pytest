# 简述

本项目是基于requests开发的一款面向 HTTP/GRPC 协议的测试工具，通过对JSON文件对维护，实现接口参数自动组合，接口自动化测试的测试需求

主要使用场景是对单接口或者有继承关系的接口进行测试

## 为什么要做这个

1. 使用postman等工具时，觉得图形化的界面使用不够迅速
2. 使用unittset或者pytest进行用例编写时又觉得重复的代码写的太多了
3. 后面了解到了httprunner，在实际使用的时候偶尔会遇到一些问题，或者自己有特殊的需求时改造别人的代码成本较高
4. 业务中遇到的一些接口需要能对参数进行组合，希望这个参数组合和发起调用两个过程可以一起执行


## 安装方式

```
pip3 install auto_generation_pytest
```

## cli命令说明
- init：初始化项目，同时生成demo文件，当前目录下已经存在的文件不会重复生成
- make：根据配置生成pytest代码
- run：直接按照配置进行接口测试，同pytest可以使用 :: 分割指定用例，如 mat run demo.json::test::test


## 环境变量配置说明

默认存在的四个环境变量值为：
- HOST: http接口测试的host

- GRPCOX: grpcox服务的地址，在进行grpc测试时使用了grpcox做中间层，如果需要进行grpc测试则这里需要进行该服务的地址配置

- GRPCOX_FROMAT: 对grpc接口返回值进行处理时调用的函数，参数值为 json|指定函数地址，函数地址按照路径用.进行分割，如：util.grpc_format.load，不配置时接口直接返回原始数据

- HTTP_FROMAT: 对http接口返回值进行处理时调用的函数，参数值为 json|指定函数地址，函数地址按照路径用.进行分割，如：util.http_format.load，不配置时接口直接返回原始数据

## 环境变量调用说明

配置文件中默认仅存在明文信息，如果需要在配置文件中使用环境变量，需要修改文件结构为：

```
{
     "Config": {
         "url": "env('GRPC_HOST')"
     },
     "TestCase": {
        "Demo": {
            "url": "$url"
     }
}
```
环境变量需要在【Config】字段中配置，在【TestCase】中使用$调用

如果不需要使用环境变量，则不需要【Config】，【TestCase】两个字段，直接进行接口测试配置即可


## 接口信息基本配置说明

http接口：
```
{pytest_class_name}: {
    "name": 接口路由地址,
    "feature": allure报告的 feature字段,
    "method":当前接口的请求方式（post，get等),
    "head": 当前接口的请求头配置,
    "process": 具体的测试场景配置
```

grpc接口：
```
{pytest_class_name}: {
    "url": 接口请求地址，如果是在集群中部署则是服务名称,
    "proto": proto文件地址,
    "server": 待测grpc server名称,
    "request": 待测grpc request名称,
    "feature": allure报告的 feature字段,
    "method": 默认使用【grpc】
    "process": 具体的测试场景配置
```

## 测试场景配置说明:
```
{用例场景分类}: {
    "fixture": pytest内置的fixture方法，因支持同时使用多个fixture，这里需要传入一个list,
    "hooks": 正式发起请求前如对参数的需要进行处理（如加密），需要把处理参数的函数名配置到这里，默认从hook目录下的hook.py导入，同样是传入list,
    "case": [
        {
            "data": 是该场景的静态数据，就是当前场景下固定的值,
            "var": 是该场景的动态数据，就是当前场景下数值会有变动的参数，配置到这里的变量会按照配置指定的方式进行组合,
            "comb": 是**动态**数据的组合方式，目前有三种：allpairs,normal,multiply
        }
    ],
    "inherit": [
        {
            "api": 如果该接口有进行接口数据的继承，此处配置继承的接口的classname},
            "process": 该class下具体继承的的process，配置process的目的继承断言和把接口之间的参数进行笛卡尔积,
            "case": 可指定具体的请求参数，该值不为空的时候,
            "data": {继承值},
        }
    ],
    "severity": allure报告的 severity字段,
    "story": allure报告的 story,
    "assert": 该场景的断言配置，配置断言函数时默认从assert_function目录下的assert_function.py导入
}
```

- allpairs: 对动态数据进行2因子交互的正交组合
- normal: 每一个参数都需要为list，且数据长度必须一致，会按照下标对动态数据一一组合
- multiply: 对动态数据进行笛卡尔积

## 接口配置方式优化

除了直接把process下的每一个场景配置和接口信息配置在同一个场景外，可以使用如下方式优化：
```
{   
    "url": "$url",
    "proto": "$path",
    "feature": "创建grpc接口测试",
    "method": "$method",
    "server": "demo.test",
    "request": "demo",
    "process": {
        "Success": {
            "story": "test",
            "path": "./process/demo/Success.json"
        }
    }
}
```
配置**path**参数后，json数据会从配置的路径进行加载，并和dict里的其他数值进行组合