# -*- coding: utf-8 -*-
# author: pengr

'''
sspider 通用实现
~~~~~~~~~~~~

commons模块下是对spider模块下的接口的通用实现，可直接对commons下的模块组件进行扩展，也可以对spider下的接口直接继承实现
'''

from .spider import AbstractSpider, AbstractDownloader, AbstractParser, AbstractRequestManager, AbstractWritter, AbstractLogger
from requests.models import Response as ParentResponse
from requests import sessions
from lxml import html
from .utils import typeassert, synchronized
import copy
import os
import re
import demjson
import json
import time


'''
    此模块为对spider模块中抽象架构的通用实现，并确定了传递对象数据结构为Reqeust对象与Response对象，各位在扩展时使用common下的包时需要按照此包下的数据结构进行通信
'''


class Request(object):

    '''
    请求对象

    @member :: method : 请求方法，有GET、POST、PUT、DELETE、OPTION \n
    @member :: url : 请求url \n
    @member :: params : 请求参数 \n
    @member :: data : 请求body数据 \n
    @member :: headers : 请求headers \n
    @member :: cookies : cookies \n
    @member :: files : files \n
    @member :: auth : auth \n
    @member :: timeout : timeout \n
    @member :: allow_redirects : allow_redirects \n
    @member :: proxies : 代理，为字典结构，{'http':'10.10.154.23:10002','https':'10.10.154.23:10004'} \n
    @member :: hooks : hooks \n
    @member :: stream : stream \n
    @member :: verify : verify \n
    @member :: cert : cert \n
    @member :: json : json \n
    @member :: level : level \n


    通常开始爬虫时，我们需要初始化一个Request对象或者一组request对象。

    初始化Request对象，必须初始化其请求方法method与请求url，其余可选
    `request = Request('get','http://www.baidu.com')`

    带有请求头的Request对象
    `headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}`
    `request = Request('get','http://www.baidu.com', headers=headers)`
    '''

    __attrs__ = [
        'method', 'url', 'params', 'data', 'headers', 'cookies', 'files',
        'auth', 'timeout', 'allow_redirects', 'proxies', 'hooks', 'stream',
        'verify', 'cert', 'json', 'level'
    ]

    def __init__(self, method, url,
                 params=None, data=None, headers=None, cookies=None, files=None,
                 auth=None, timeout=None, allow_redirects=True, proxies=None,
                 hooks=None, stream=None, verify=None, cert=None, json=None,
                 level=1, other_info=None, sleep_time=None):
        self.method = method
        self.url = url
        self.params = params
        self.data = data
        self.headers = headers
        self.cookies = cookies
        self.files = files
        self.auth = auth
        self.timeout = timeout
        self.allow_redirects = allow_redirects
        self.proxies = proxies
        self.hooks = hooks
        self.stream = stream
        self.verify = verify
        self.cert = cert
        self.json = json
        self.level = level
        self.other_info = other_info
        self.sleep_time = sleep_time

    def __getitem__(self, item):
        return getattr(self, item)

    def transRequestParam(self):
        params = copy.copy(self.__dict__)
        params.pop('level')
        params.pop('other_info')
        params.pop('sleep_time')
        return params


class Response(ParentResponse):

    '''
    响应对象

    @member :: _content : 响应二进制数据 \n
    @member :: _content_consumed : _content_consumed \n
    @member :: _next : _next \n
    @member :: status_code : 响应状态码 \n
    @member :: headers : 响应头 \n
    @member :: raw : raw \n
    @member :: url : 请求url \n
    @member :: encoding : 响应编码 \n
    @member :: history : 响应历史 \n
    @member :: reason : reason \n
    @member :: cookies : 响应cookies \n
    @member :: elapsed : elapsed \n
    @member :: request : request \n
    @member :: level : 对应request的level \n
    '''

    def __init__(self, request, cls=None, **kwargs):
        if cls:
            self._content = cls._content
            self._content_consumed = cls._content_consumed
            self._next = cls._next
            self.status_code = cls.status_code
            self.headers = cls.headers
            self.raw = cls.raw
            self.url = cls.url
            self.encoding = cls.encoding
            self.history = cls.history
            self.reason = cls.reason
            self.cookies = cls.cookies
            self.elapsed = cls.elapsed
        else:
            super().__init__(**kwargs)
        self.request = request
        self.level = request.level

    def __getitem__(self, item):
        return getattr(self, item)

    def jsonp(self):
        '''
        将jsonp格式的response解析为json对象
        '''
        return demjson.decode(
            re.match(".*?({.*}).*", self.text, re.S).group(1))

    def html(self, encoding=None, **kwargs):
        '''
        将response解析为HtmlElement对象，可通过css选择器或者xpath语法获取数据

        如：
            >>> doc = response.html()
            >>> # 通过xpath获取a元素里的href
            >>> links = doc.xpath('//a/@href')
            >>> # 通过xpath获取span元素中的text
            >>> spans = doc.xpath('//span/text()')
            >>> # 更多用法，请自行查询css选择器与xpath语法进行使用

            常用方法：
            find, findall, findtext, get, getchildren, getiterator, getnext, getparent, getprevious, getroottree, index, insert, items, iter, iterancestors, iterchildren, iterdescendants, iterfind, itersiblings, itertext, keys, makeelement, remove, replace, values, xpath

            >>> .drop_tree():
            Drops the element and all its children. Unlike el.getparent().remove(el) this does not remove the tail text; with drop_tree the tail text is merged with the previous element.
            >>> .drop_tag():
            Drops the tag, but keeps its children and text.
            >>> .find_class(class_name):
            Returns a list of all the elements with the given CSS class name. Note that class names are space separated in HTML, so doc.find_class_name('highlight') will find an element like <div class="sidebar highlight">. Class names are case sensitive.
            >>> .find_rel_links(rel):
            Returns a list of all the <a rel="{rel}"> elements. E.g., doc.find_rel_links('tag') returns all the links marked as tags.
            >>> .get_element_by_id(id, default=None):
            Return the element with the given id, or the default if none is found. If there are multiple elements with the same id (which there shouldn't be, but there often is), this returns only the first.
            >>> .text_content():
            Returns the text content of the element, including the text content of its children, with no markup.
            >>> .cssselect(expr):
            Select elements from this element and its children, using a CSS selector expression. (Note that .xpath(expr) is also available as on all lxml elements.)
            >>> .label:
            Returns the corresponding <label> element for this element, if any exists (None if there is none). Label elements have a label.for_element attribute that points back to the element.
            >> .base_url:
            The base URL for this element, if one was saved from the parsing. This attribute is not settable. Is None when no base URL was saved.
            >>> .classes:
            Returns a set-like object that allows accessing and modifying the names in the 'class' attribute of the element. (New in lxml 3.5).
            >>> .set(key, value=None):
            Sets an HTML attribute. If no value is given, or if the value is None, it creates a boolean attribute like <form novalidate></form> or <div custom-attribute></div>. In XML, attributes must have at least the empty string as their value like <form novalidate=""></form>, but HTML boolean attributes can also be just present or absent from an element without having a value.
        '''
        if not self.encoding and self.content and len(self.content) > 3:
            if encoding is not None:
                try:
                    return html.fromstring(
                        self.content.decode(encoding), **kwargs
                    )
                except UnicodeDecodeError:
                    pass
        return html.fromstring(self.text, **kwargs)


class HtmlDownloader(AbstractDownloader):

    """
    下载器

    对传入的请求进行请求下载

    @member :: timeout : 下载超时时间

    对与下载器下载前后，很多时候都需要进行一些扩展中间件，在此框架中，可以运用装饰者模式对其进行扩展，也可以自己继承实现 AbstractDownloader 接口中的方法。

    例如：通过装饰器实现添加代理

        >>> # 我们需要一个代理池（可将代理池设置为单例类），类似与requestManager.假定我们得代理池如下：
        >>> class ProxyPool(object):
        >>>     def get_new_proxy:
        >>>         '''
        >>>         请求代理，返回一个可用的、未被使用过的代理
        >>>             return proxy
        >>>         '''
        >>>         passs
        >>> def proxyWrapper():
        >>>     '''
        >>>     通过装饰器给请求动态添加代理
        >>>     '''
        >>> def decorate(func):
        >>>         @wraps(func)
        >>>         def wrapper(request):
        >>>             proxy = ProxyPool().get_new_proxy()
        >>>             request.proxy = proxy
        >>>             return func(*args, **kwargs)
        >>>         return wrapper
        >>>     return decorate

        完成代理的装饰器后可直接在 download 方法中进行使用：


        >>> @typeassert(request=Request)
        >>> @proxyWrapper
        >>> def download(self, request):
        >>>     with sessions.Session() as session:
        >>>         return Response(request, cls=session.request(**request.TransRequestParam()))

    同样的，也可以将下载单元加入单线程、多进程进行下载请求资源，这样就与解析异步进行，提高爬取效率
    对于cookie，请求头等的设置类似上面代理装饰器

    """

    @typeassert(request=Request)
    def download(self, request):
        if request.sleep_time:
            time.sleep(request.sleep_time)
        with sessions.Session() as session:
            return Response(request, cls=session.request(**request.transRequestParam()))


class HtmlParser(AbstractParser):

    '''
    解析器

    对传入的文本进行解析

    在爬取网页中，这部分时很难统一的，各个网站有不同的特色，所以此部分是一般需要用户自己独立重写的
    '''

    @typeassert(response=Response)
    def parse(self, response):
        htm = response.html()
        requests = []
        for item in htm.iter('a'):
            request = copy.copy(response.request)
            request.method = 'get'
            request.url = item.get('href')
            request.level = response.level+1
            request.timeout = 3
            requests.append(request)
        datas = [text.strip() for text in htm.itertext()]
        return requests, datas


import hashlib


class RequestManager(AbstractRequestManager):

    '''
    请求管理器

    管理所有的请求
    '''

    def __init__(self, limit_level=1):
        '''
        请求管理器初始化函数

            @param :: limit_level : 爬取层数限制，默认限制3层 \n
            @member :: level : 当前爬取层数 \n
            @member :: new_requests : 未爬取请求集合，采用字典存储，key对应相应的层数，value相应层数未请求的请求集合 \n
            @member :: old_requests : 已存储请求集合，采用元组存储，每个请求计算128位md5码进行存储 \n
            @member :: limit_level : 爬取层数限制，默认限制3层 \n

        '''
        self.__level = 1
        self.__new_requests = {}
        self.__old_requests = set()
        self.__limit_level = limit_level

    @typeassert(request=Request)
    def add_new_request(self, request):
        '''
        添加请求

            @param :: request : Request请求

            return : None

        '''
        if not request in self.__old_requests:
            self.__add_new_request(request)
            self.__add_old_request(request)

    def has_new_request(self, level=None):
        '''
        判断是否还有待爬取的请求，当传入level后，判断相应的层数中是否还有待爬取的请求。默认判断所有层数

            @param :: level : 待添加请求集合

            return : Bool

        '''
        return self.new_requests_size(level) > 0

    def get_new_request(self, level=None):
        '''
        获取一个未被请求过的请求

            @param :: level : 从指定层数中提取，默认为None

            return : request

        '''
        if not self.has_new_request(level):
            return

        if len(self.__new_requests[str(self.__level)]) <= 0:
            self.__add_level()

        if not level:
            level = self.__level
        return self.__get_new_request(level)

    @property
    def level(self):
        '''
        获取当前层级

            return : int

        '''
        return self.__level

    def new_requests_size(self, level=None):
        '''
        待爬取的请求集合长度

            @param :: level : 获取指定层数的请求集合长度

            return : int

        '''
        if level:
            return self.__new_request_size(level)
        else:
            return sum(map(lambda x: self.__new_request_size(x), self.__new_requests))

    def old_requests_size(self):
        '''
        已请求的请求集合长度

            @param :: level : 获取指定层数的请求集合长度

            return : int

        '''
        return len(self.__old_requests)

    def __add_level(self,):
        '''
        (私有函数)增加当前爬取层数

            return : None

        '''
        self.__level += 1

    def __init_level(self, level):
        '''
        (私有函数)初始化level层的待爬取请求集合

            @param :: level : 指定要初始化的level层

            return : None

        '''
        if not str(level) in self.__new_requests:
            self.__new_requests[str(level)] = set()

    def __add_new_request(self, request):
        '''
        (私有函数)添加请求,向未爬取过的请求集合中添加请求

            @param :: requests : 待添加请求

            return : None

        '''
        if request.level > self.__limit_level:
            return

        if not str(self.__level) in self.__new_requests:
            self.__init_level(self.__level)

        if not str(request.level) in self.__new_requests:
            self.__init_level(request.level)

        self.__new_requests[str(request.level)].add(request)

    def __add_old_request(self, request):
        '''
        (私有函数)添加请求,向已爬取过的请求集合中添加请求。集合中添加请求文本的128位md5码

            @param :: request : 待添加请求文本

            return : None

        '''
        md5 = hashlib.md5()
        md5.update(request.__str__().encode('utf-8'))
        self.__old_requests.add(md5.hexdigest()[8:-8])

    def __get_new_request(self, level):
        '''
        (私有函数)获取一个未被请求过的请求

            @param :: level : 从指定层数中提取

        '''
        if str(level) in self.__new_requests and self.__new_requests[str(level)]:
            return self.__new_requests[str(level)].pop()

    def __new_request_size(self, level):
        '''
        (私有函数)获取level层未爬取的请求集合长度

            @param :: level : 从指定层数中提取

            return : int

        '''
        if str(level) in self.__new_requests:
            return len(self.__new_requests[str(level)])
        return 0


import pickle


class CommonWritter(AbstractWritter):

    '''
    数据写入类

    将数据以特定格式写入到磁盘中
    self.mode = 'append' or 'extend'


    对于字典格式的数据支持：

        >>> from sspider import Request, Spider, RequestManager, HtmlParser, TxtWritter, JsonWritter
        >>> url ='https://www.easy-mock.com/mock/5c749b5e0d6f122f99e20e72/example/datadict'
        >>> #建立自定义parser
        >>> class MyParser(HtmlParser):
        >>>     def parse(self, response):
        >>>         data = response.json()['data']
        >>>         # 打印解析数据
        >>>         print(data)
        >>>         return [],data
        >>> # 构建初始请求集合
        >>> reqs = [Request('get',url) for i in range(4)]
        >>> # 写入类对象
        >>> writter = TxtWritter()
        >>> # 建立爬虫对象
        >>> spider = Spider(writter = writter,parser=MyParser())
        >>> # 建立爬虫
        >>> spider.run(reqs)
        >>> #写入数据
        >>> spider.write('test.txt')
        >>> #查看字典数据头部
        >>> print(writter.headers)
    '''

    class WritterMode(object):
        APPEND = 'append'
        EXTEND = 'extend'

    def __init__(self, writeMode=WritterMode.APPEND):
        super().__init__()
        self._items = []
        self._headers = {}
        self._buffer_file = 'buffer_'+self.__class__.__name__+'.txt'
        self.writeMode = writeMode
        self.max_buffer = 1000

    @property
    def items(self):
        '''
        获取所有爬取到的数据
        '''
        if not os.path.exists(self._buffer_file):
            return self._items
        items = []
        with open(self._buffer_file, 'rb') as f:
            try:
                while True:
                    items.append(pickle.load(f))
            except EOFError:
                pass
        items.extend(self._items)
        return items

    @property
    def headers(self):
        '''
        获取数据头部
        '''
        return list(self._headers.values())

    @headers.setter
    def headers(self, headers):
        if isinstance(headers, list):
            self._headers = {h: h for h in headers}
        elif isinstance(headers, dict):
            self._headers = headers
        else:
            raise ValueError('未知类型的headers')

    def insert(self, data, index=0):
        self._items.insert(index, data)

    def write(self, filename, data=None, write_header=False,):
        if data is None:
            data = copy.copy(self.items)
        if write_header:
            data.insert(0, self.headers)
        return data

    @synchronized
    def write_buffer(self, item):
        if self.writeMode == self.WritterMode.EXTEND:
            for i in item:
                self.__addItem(i)
        elif self.writeMode == self.WritterMode.APPEND:
            self.__addItem(item)
        else:
            raise AttributeError("非法的writeMode,"+self.mode)

    @synchronized
    def flush_buffer(self):
        if len(self._items) == 0:
            return
        with open(self._buffer_file, 'ab+') as f:
            for item in self._items:
                pickle.dump(item, f)
        del self._items[:]

    @synchronized
    def remove_buffer(self):
        if os.path.exists(self._buffer_file):
            os.remove(self._buffer_file)

    def __addItem(self, item):
        if isinstance(item, dict):
            item = self.__dictToList(item)

        self.__addListItems(item)
        if len(self._items) > self.max_buffer:
            self.flush_buffer()

    def __dictToList(self, dictItems):
        for key in dictItems:
            if key not in self._headers:
                self._headers[key] = key
        tempList = []
        for k in self._headers:
            if k in dictItems:
                tempList.append(dictItems[k])
            else:
                tempList.append('')
        return tempList

    def __addListItems(self, listItems):
        self._items.append(listItems)

    def __del__(self):
        self.remove_buffer()


class TxtWritter(CommonWritter):

    '''
    txt格式写数据

    将每个网页中的数据作为一个item对象，直接将该对象写入到文件中。

    示例：

        >>> from sspider import Spider, RequestManager, Request, HtmlParser, TxtWritter
        >>> # 建立请求对象
        >>> req = Request(
            'get', 'https://www.easy-mock.com/mock/5c749b5e0d6f122f99e20e72/example/data')
        >>> # 构建特定的解析器
        >>> class Myparser(HtmlParser):
        >>>     def parse(self, response):
        >>>         return [req], response.json()['data']
        >>> # 构建TxtWritter对象
        >>> txtWritter = TxtWritter()
        >>> # 构架爬虫对象
        >>> spider = Spider(parser=Myparser(),
                        requestManager=RequestManager(4), writter=txtWritter)
        >>> # 运行爬虫
        >>> spider.run(req)
        >>> # 数据写入test文件
        >>> spider.write("test.txt")
    '''

    def write(self, filename, data=None, mode='w+', encode='utf-8', write_header=True):
        data = super().write(filename, data, write_header)
        with open(filename, mode, encoding=encode) as f:
            for item in data:
                f.write(str(item))
                f.write('\n')


class NonWritter(AbstractWritter):
    def write(self, *args, **kwargs):
        pass

    def write_buffer(self, item):
        pass

    def flush_buffer(self):
        pass


class JsonWritter(CommonWritter):

    '''
    json格式写数据

    将数据以json格式写入数据文件中

    示例：

        >>> from sspider import Spider, RequestManager, Request, HtmlParser, JsonWritter
        >>> # 建立请求对象
        >>> req = Request(
            'get', 'https://www.easy-mock.com/mock/5c749b5e0d6f122f99e20e72/example/data')
        >>> # 构建特定的解析器
        >>> class Myparser(HtmlParser):
        >>>     def parse(self, response):
        >>>         return [req], response.json()['data']
        >>> # 构建JsonWritter对象
        >>> jsonWritter = JsonWritter()
        >>> # 构架爬虫对象
        >>> spider = Spider(parser=Myparser(),
                        requestManager=RequestManager(4), writter=jsonWritter)
        >>> # 运行爬虫
        >>> spider.run(req)
        >>> # 数据写入test文件
        >>> spider.write("test.json")
    '''

    def write(self, filename, data=None, mode='w+', encode='utf-8', write_header=True):
        data = super().write(filename, data, write_header)
        with open(filename, mode, encoding=encode) as f:
            f.write(json.dumps(data, indent=4, separators=(
                ',', ': '), ensure_ascii=False))


import csv


class CsvWritter(CommonWritter):

    '''
    csv格式写数据

    将数据以csv格式写入数据文件中

    示例：

          >>> from sspider import Spider, RequestManager, Request, HtmlParser, CsvWritter
        >>> # 建立请求对象
        >>> req = Request(
            'get', 'https://www.easy-mock.com/mock/5c749b5e0d6f122f99e20e72/example/data')

        >>> # 构建特定的解析器
        >>> class Myparser(HtmlParser):
        >>>     def parse(self, response):
        >>>         return [req], response.json()['data']
        >>> # 构建CsvWritter对象
        >>> csvWritter = CsvWritter()
        >>> # 构架爬虫对象
        >>> spider = Spider(parser=Myparser(),
                        requestManager=RequestManager(4), writter=csvWritter)
        >>> # 运行爬虫
        >>> spider.run(req)
        >>> # 数据写入test文件
        >>> spider.write("test.csv")
    '''

    def write(self, filename, data=None, mode='w+', encode='utf-8', write_header=True):
        '''
        csv格式写入，写入数据格式为二维结构，即二维列表
            @param :: items : 数据序列
            return : None
        '''
        data = super().write(filename, data, write_header)
        with open(filename, mode, encoding=encode, newline='') as f:
            csvfile = csv.writer(f)
            for item in data:
                csvfile.writerow(item)


from xlwt import Workbook


class XlsWritter(CommonWritter):

    '''
    xls格式写数据

    将数据以xls格式写入数据文件中

    示例：

          >>> from sspider import Spider, RequestManager, Request, HtmlParser, XlsWritter
        >>> # 建立请求对象
        >>> req = Request(
            'get', 'https://www.easy-mock.com/mock/5c749b5e0d6f122f99e20e72/example/data')
        >>> # 构建特定的解析器
        >>> class Myparser(HtmlParser):
        >>>     def parse(self, response):
        >>>         return [req], response.json()['data']
        >>> # 构建XlsWritter对象
        >>> xlsWritter = XlsWritter()
        >>> # 构架爬虫对象
        >>> spider = Spider(parser=Myparser(),
                        requestManager=RequestManager(4), writter=xlsWritter)
        >>> # 运行爬虫
        >>> spider.run(req)
        >>> # 数据写入test文件
        >>> spider.write("test.xls")
    '''

    def write(self, filename, data=None, mode='w+', encode='utf-8', write_header=True):
        '''
        xls格式写入，写入数据格式为二维结构，即二维列表
            @param :: items : 数据序列
            return : None
        '''
        data = super().write(filename, data, write_header)
        book = Workbook()
        worksheet = book.add_sheet("Sheet 1")
        row = 0
        col = 0
        for item in data:
            for i in item:
                worksheet.write(row, col, str(i))
                col += 1
            row += 1
            col = 0
            if row > 65535:
                book.save(filename)
                raise OverflowError(
                    "Hit limit of #of rows in one sheet(65535).")
        book.save(filename)


import xlsxwriter


class XlsxWritter(CommonWritter):

    '''
    xlsx格式写数据

    将数据以xlsx格式写入数据文件中

    示例：

        >>> from sspider import Spider, RequestManager, Request, HtmlParser, XlsxWritter
        >>> # 建立请求对象
        >>> req = Request(
            'get', 'https://www.easy-mock.com/mock/5c749b5e0d6f122f99e20e72/example/data')

        >>> # 构建特定的解析器
        >>> class Myparser(HtmlParser):
        >>>     def parse(self, response):
        >>>         return [req], response.json()['data']
        >>> # 构建XlsxWritter对象
        >>> xlsxWritter = XlsxWritter()
        >>> # 构架爬虫对象
        >>> spider = Spider(parser=Myparser(),
                        requestManager=RequestManager(4), writter=xlsxWritter)
        >>> # 运行爬虫
        >>> spider.run(req)
        >>> # 数据写入test文件
        >>> spider.write("test.xlsx")
    '''

    def write(self, filename, data=None, mode='w+', encode='utf-8', write_header=True):
        '''
        xlsx格式写入，写入数据格式为二维结构，即二维列表
            @param :: items : 数据序列
            return : None
        '''
        data = super().write(filename, data, write_header)
        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet()
        row = 0
        col = 0
        for item in data:
            for i in item:
                worksheet.write(row, col, str(i))
                col += 1
            row += 1
            col = 0

        workbook.close()


import logging
from .utils import set_color, FOREGROUND_GREEN, FOREGROUND_YELLOW, FOREGROUND_BLUE, FOREGROUND_RED, FOREGROUND_WHITE


class Logger(AbstractLogger):

    __instance_name = {}

    def __init__(self, name, path=None, clevel=logging.DEBUG, Flevel=logging.DEBUG):
        '''
        日志类

            @param :: name : 日志名称
            @member :: clevel : 打印控制台级别
            @member :: Flevel : 输出日志文件级别

        '''
        if name in self.__instance_name:
            self.__instance_name[name] += 1
            name = "{}-{}".format(name, self.__instance_name[name])
        else:
            self.__instance_name[name] = 0
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        fmt = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')
        # 设置CMD日志
        sh = logging.StreamHandler()
        sh.setFormatter(fmt)
        sh.setLevel(clevel)
        # 设置文件日志
        if path is None:
            path = os.getcwd()+'\\'+name+'.log'
        fh = logging.FileHandler(path)
        fh.setFormatter(fmt)
        fh.setLevel(Flevel)
        self.logger.addHandler(fh)
        self.logger.addHandler(sh)

    def debug(self, message):
        self.logger.debug(message)

    @set_color(FOREGROUND_GREEN)
    def info(self, message):
        self.logger.info(message)

    @set_color(FOREGROUND_YELLOW)
    def warn(self, message):
        self.logger.warn(message)

    @set_color(FOREGROUND_RED)
    def exception(self, message):
        self.logger.exception(message)

    @set_color(FOREGROUND_RED)
    def error(self, message):
        self.logger.error(message)

    def cri(self, message):
        self.logger.critical(message)


class Spider(AbstractSpider):

    def __init__(self, name=None, downloader=HtmlDownloader(), parser=HtmlParser(), requestManager=RequestManager(), writter=CommonWritter(), logger=None):
        self.name = name if name is not None else self.__class__.__name__
        logger = logger if logger is not None else Logger(self.name)
        super().__init__(downloader=downloader, parser=parser,
                         requestManager=requestManager, writter=writter, logger=logger)

    def run(self, requests):
        '''
        运行爬虫，需要传入初始url或者初始请求或者初始请求集合
        示例：
            >>> from sspider import Spider
            >>> url = 'http://www.baidu.com'
            >>> spider = Spider()
            >>> spider.run(url)
            ... 或者
            >>> from sspider import Spider
            >>> req = {
                        'url':url,
                        'method':'get'
                    }
            >>> spider = Spider()
            >>> spider.run(req)
            ... 或者
            >>> from sspider import Spider
            >>> initUrls = ['http://www.baidu.com','http://www.baidu.com']
            >>> spider = Spider()
            >>> spider.run(initUrls)
            ... 或者
            >>> from sspider import Spider
            >>> reqs = [{
                        'url':url,
                        'method':'get'
                    },{
                        'url':url,
                        'method':'get'
                    }]
            >>> spider = Spider()
            >>> spider.run(reqs)
        '''
        if not isinstance(requests, list):
            requests = [requests]
        new_requests = []
        for req in requests:
            if isinstance(req, Request):
                new_requests.append(req)
            elif not isinstance(req, Request) and isinstance(req, dict):
                new_requests.append(Request(**req))
            elif not isinstance(req, Request) and isinstance(req, str):
                new_requests.append(Request('get', req))
            else:
                raise ValueError('传入非法请求！')
        super().run(new_requests)

    def write(self, filename, mode='w+', encode='utf-8', write_header=False):
        '''
        将数据写入磁盘，依赖于初始化Spider时的writter，默认为CommonWritter，即将数据打印到控制台
        '''
        self.writter.write(filename, None,  mode=mode,
                           encode=encode, write_header=write_header)

    def getItems(self, type='list'):
        '''
        获取抓取到的数据
        '''
        if type == 'list':
            for item in self.writter.items:
                yield item
        if type == 'dict':
            for data in self.writter.items:
                item = {}
                i = 0
                for key in self.writter.headers:
                    item[key] = data[i]
                    i += 1
                yield item
