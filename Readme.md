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

[中文](./Readme-zh.md)

## Overview

A simple web crawling framework.[Document](https://duiliuliu.github.io/simple-spiders/)

## Getting Started

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

## Referenced Document

- [Project document](https://duiliuliu.github.io/simple-spiders/)
- Blog document
  - [自己写python爬虫框架(一)](https://duiliuliu.github.io/2019/04/10/%E8%87%AA%E5%B7%B1%E5%86%99python%E7%88%AC%E8%99%AB%E6%A1%86%E6%9E%B6%E4%B8%80/)
  - [自己写python爬虫框架(二)-下载器](https://duiliuliu.github.io/2019/04/11/%E8%87%AA%E5%B7%B1%E5%86%99python%E7%88%AC%E8%99%AB%E6%A1%86%E6%9E%B6%E4%BA%8C/)
  - [自己写python爬虫框架(三)-解析器](https://duiliuliu.github.io/2019/04/13/%E8%87%AA%E5%B7%B1%E5%86%99python%E7%88%AC%E8%99%AB%E6%A1%86%E6%9E%B6%E4%B8%89/)
  - [自己写python爬虫框架(四)-请求管理器](https://duiliuliu.github.io/2019/04/16/%E8%87%AA%E5%B7%B1%E5%86%99python%E7%88%AC%E8%99%AB%E6%A1%86%E6%9E%B6%E5%9B%9B/)

## Referenced Libraries

- Using [requests](https://github.com/requests/requests) as htmlDownloader
- Using [lxml](https://github.com/lxml/lxml) as default htmlParser
- Using [csv](http://www.python-csv.org) provide feature that export file as csv type
- Using [xlwt](http://www.python-excel.org/) provide feature that export file as excel type
- Using [xlsxwriter](https://xlsxwriter.readthedocs.io) provide feature that export file as xexcel type

## Project structure

```

```

## License

This project is published open source under ![license](./images/license-LGPL--3.0-orange.svg) agreement. Please maintain the open source release after modification and sign the name of the original author. Thank you for your respect

If you need to apply this project for commercial purposes, please contact me( [@pengr](https://github.com/duiliuliu) ) separately to obtain commercial authorization
