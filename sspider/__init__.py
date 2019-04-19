# -*- coding: utf-8 -*-
# author: pengr

#      _              _       ___       _    _
#  ___<_>._ _ _  ___ | | ___ / __> ___ <_> _| | ___  _ _
# <_-<| || ' ' || . \| |/ ._>\__ \| . \| |/ . |/ ._>| '_>
# /__/|_||_|_|_||  _/|_|\___.<___/|  _/|_|\___|\___.|_|
#               |_|               |_|


'''
sspider
~~~~~~~~~~~~

simpleSpider，快速开始：

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

... 或者我们按照需求初始化Spider

   >>> from sspider import Spider, Request, RequestManager, TxtWritter
   >>> request = Request('get', 'https://movie.douban.com/subject/27202819/reviews')
   >>> # 设置爬取深度为2，进行爬取
   >>> requestManager = RequestManager(2)
   >>> txtWritter = TxtWritter()
   >>> spider = Spider(requestManager=requestManager, writter=txtWritter)
   >>> spider.run(request)
   >>> print(len(spider.getItems()))
   >>> spider.write('test.txt')
   >>> # 可以看到数据保存到了test.txt中

:copyright: (c) 2018 by pengr.
:license: GNU GENERAL PUBLIC LICENSE, see LICENSE for more details.
'''


from . import utils
from . import spider
from .commons import Spider, Request, Response, HtmlDownloader, HtmlParser, RequestManager,  Logger
from .commons import TxtWritter, CsvWritter, JsonWritter, XlsWritter, XlsxWritter, CommonWritter


from .__version__ import __title__, __description__, __url__, __version__
from .__version__ import __author__, __author_email__
from .__version__ import __copyright__
