加油站系统介绍

写着玩的，天天加油，好多东西再不写，就荒废了，内容太过lowB，纯属练练手

有两个系统，一开始是dos系统，一键分析execl表格，然后根据液位高度算出油罐有多少升油，展示数据

![dos系统首页图片](https://github.com/exampleK/oil-dos-and-tornado-system/blob/master/img/dos.jpg)

然后第二个系统是用，忘了说，两个系统都是python3写的，第二个后台框架是tornado写的 mysql 数据库，前台找的模板插的数据，莫的东西，就是数据处理麻烦的很

就如下图展示的数据一样，通过 上传execl表格 然后自动分析数据 插到 数据库里 前台 展示数据

![前台首页图片](https://github.com/exampleK/oil-dos-and-tornado-system/blob/master/img/d2.jpg)

上传分析api 下图

![上传](https://github.com/exampleK/oil-dos-and-tornado-system/blob/master/img/1.jpg)

液位计算api 下图

![液位计算](https://github.com/exampleK/oil-dos-and-tornado-system/blob/master/img/2.jpg)