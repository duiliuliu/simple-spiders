# simple Spider

![python -> 3.4+](./images/python-3.4+-green.svg)
![coverage -> 37%](https://img.shields.io/badge/coverage-37%25-yellowgreen.svg)
![build -> passing](./images/build-passing-orange.svg)

```
     _              _       ___       _    _
 ___<_>._ _ _  ___ | | ___ / __> ___ <_> _| | ___  _ _
<_-<| || ' ' || . \| |/ ._>\__ \| . \| |/ . |/ ._>| '_>
/__/|_||_|_|_||  _/|_|\___.<___/|  _/|_|\___|\___.|_|
              |_|               |_|
```

[英文](./Readme-zh.md)

## 概述

一个简单的爬虫框架。 [详细文档](https://duiliuliu.github.io/simple-spiders/)

## 开始入门

`pip install sspider`

You should construst project.py to suit your needs

```
   >>> from sspider import Spider, Request
   >>> # 建立request对象
   >>> request = Request('get', 'https://movie.douban.com/subject/27202819/reviews')
   >>> # 建立爬虫对象
   >>> spider = Spider()
   >>> # 运行爬虫
   >>> spider.run(request)
   ...
   >>> # 保存爬取结果
   >>> spider.write('test.txt)
```

`python project.py`

`Ctrl-C to stop`

## 相关引用库

- Using [requests](https://github.com/requests/requests) as htmlDownloader
- Using [lxml](https://github.com/lxml/lxml) as default htmlParser
- Using [csv](http://www.python-csv.org) provide feature that export file as csv type
- Using [xlwt](http://www.python-excel.org/) provide feature that export file as excel type
- Using [xlsxwriter](https://xlsxwriter.readthedocs.io) provide feature that export file as xexcel type

## 项目结构

```
- crawler/
    - __init__.py
    - test/
      - htmlDownloder_test
      - htmlParser_test
      - requestManager_test
      - writter_test
      - logger_test
      - spider_test

    - htmlDownloder
    - htmlParser
    - requestManager
    - writter
    - logger
    - spider

- main.py
```

## License

本项目采用 [![license](./images/license-LGPL--3.0-orange.svg)](https://github.com/duiliuliu/simple-spiders) 协议开源发布，请您在修改后维持开源发布，并为原作者额外署名，谢谢您的尊重。

若您需要将本项目应用于商业目的，请单独联系本人( [@pengr](https://github.com/duiliuliu) )，获取商业授权。
