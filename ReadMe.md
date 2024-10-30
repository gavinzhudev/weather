# Weather项目

## 功能实现
1. 当日天气和未来三日天气预报.天气来源于高德Api,中国行政区信息来源于中国民政部.当通过下拉选中城市,或在输入栏按回车时,获取和展示天气信息.
2. 输入栏自动补全,当输入"gz","guangz","广"都会自动联想补全"广州市"

ReadMe.pdf包含示例图片

![a1](https://staic.x-labs.net/a1.png)

![a1](https://staic.x-labs.net/a2.png)

## 技术实现

1. 前端采用React,使用Create-React-APP脚手架,AntDesgin中的部分组件.天气图标信息来源于iconfont
2. 后端使用Flask,采用的package有poetry,pytest,flask_restx.

全局处理异常,包含4xx和5xx错误
绑定日志,蓝图
自定义异常类
单元测试
提供Swagger文档,位于domain/api处
给前端返回统一的格式.格式为{code_staus:xx,data:xx,message:xx}