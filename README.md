# auto_generation_pytest
根据配置自动组合参数，生成pytest代码

# 使用

基本配置和使用方式参考demo

```
{pytest_class_name}: {
        "name": {接口路由},
        "feature": {allure feature}
        "method": {requests method}
        "head": {requests head}
        "process": {
            {用例分类}: {
                "skip": false,
                "fixture": [
                    {pytest fixture}
                ],
                "hooks": [
                    {参数传递前的处理函数}
                ],
                "case": [
                    {
                        "data": {静态变量},
                        "var": {动态变量},
                        "comb": { multiply | normal | multiply }
                    }
                ],
                "inherit": [
                    {
                        "api": {继承的class},
                        "process": {该class的process},
                        "case": {可指定具体的参数},
                        "data": {继承值},
                    }
                ],
                "severity": {allure 用例级别},
                "story": {allure 用例说明},
                "assert": {断言配置}
            }
    }

```

# 具体字段说明

## process

在接口用例的分组上是按照**具有相同断言**的用例为一组（process）

## skip

对于部分被继承的process，其用例已经在子用例里全量执行过了，因此不需要重复再生成代码，这里可以配置True

## case

process.{用例名称}.case.data 是该用例的静态数据，就是变量当前场景下固定的值

process.{用例名称}.case.var  是该用例的动态数据，就是变量当前场景下数值会有变动的值

process.{用例名称}.case.comb 是**动态**数据的组合方式，目前有三种：allpairs,normal,multiply

- allpairs: 对动态数据进行2因子交互的正交组合
- normal: 每一个参数都需要为list，且数据长度必须一致，会按照下标对动态数据一一组合
- multiply: 对动态数据进行笛卡尔积

动态数据组合完成后，会把静态数据补充到最后结果中

## inhert

inhert.{class_name} 指定继承的class
inhert.{class_process} 指定继承的process
inhert.case 指定该父级接口调用时的参数，不指定时默认会使用该process下的全部参数和子代进行笛卡尔积
inhert.data 指定继承的数据，可为空

已经被用例inherit的用例，依然可以inherit其他用例，但是不能循环或者inherit自己

## assert

这里可配置函数，生成的代码默认import assert_function目录，可在该目录下配置断言函数

若配置里使用了**response**，返回值会json, 默认返回的变量名为**r**





