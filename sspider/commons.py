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
                 hooks=None, stream=None, verify=None, cert=None, json=None, level=1):
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

    def __getitem__(self, item):
        return getattr(self, item)

    def transRequestParam(self):
        params = copy.copy(self.__dict__)
        params.pop('level')
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

    def __init__(self, timeout=3):
        self.timeout = timeout

    @typeassert(request=Request)
    def download(self, request):
        request.timeout = self.timeout
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
            return None
        if not level:
            level = self.__level
        if len(self.__new_requests[str(self.__level)]) <= 1:
            self.__add_level()
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
        if not str(self.__level) in self.__new_requests:
            self.__init_level(self.__level)

        if request.level > self.__limit_level:
            return

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
    '''

    def __init__(self):
        super().__init__()
        self._items = []
        self._headers = {}
        self._buffer_file = 'buffer_'+self.__class__.__name__+'.txt'
        self.max_buffer = 10

    @property
    def items(self):
        if not os.path.exists(self._buffer_file):
            return self._items
        items = []
        items.append(self._headers.values())
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
        return self._headers.values()

    @headers.setter
    def headers(self, headers):
        if isinstance(headers, list):
            self._headers = {h: h for h in headers}
        elif isinstance(headers, dict):
            self._headers = headers
        else:
            raise ValueError('未知类型的headers')

    def write(self, filename, data=None, mode='w+', encode='utf-8'):
        if data is None:
            data = self.items

        print(data)

    @synchronized
    def write_buffer(self, item):
        if isinstance(item, list):
            self.__addListItems(item)
        elif isinstance(item, dict):
            self.__addDictItems(item)
        else:
            raise ValueError('未知类型的headers')
        if len(self._items) > self.max_buffer:
            self.flush_buffer()

    @synchronized
    def flush_buffer(self):
        if len(self._items) == 0:
            return
        with open(self._buffer_file, 'wb+') as f:
            for item in self._items:
                pickle.dump(item, f)
        del self._items[:]

    @synchronized
    def remove_buffer(self):
        if os.path.exists(self._buffer_file):
            os.remove(self._buffer_file)

    def __addDictItems(self, dictItems):
        tempHeaders = {key: key for key in dictItems}
        tempHeaders.update(self._headers)
        self._headers = tempHeaders
        tempList = []
        for k in self._headers:
            if k in dictItems:
                tempList.append(dictItems[k])
            else:
                tempList.append('')
        self._items.append(tempList)

    def __addListItems(self, listItems):
        self._items.append(listItems)

    def __del__(self):
        self.remove_buffer()


class TxtWritter(CommonWritter):

    def write(self, filename, data=None, mode='w+', encode='utf-8'):
        if data is None:
            data = self.items
        with open(filename, mode, encoding=encode) as f:
            for item in data:
                f.write(' | '.join(str(i) for i in item)+'\n')


import logging
from .utils import set_color, FOREGROUND_GREEN, FOREGROUND_YELLOW, FOREGROUND_BLUE, FOREGROUND_RED, FOREGROUND_WHITE


class Logger(AbstractLogger):

    def __init__(self, name, path=None, clevel=logging.DEBUG, Flevel=logging.DEBUG):
        '''
        日志类

            @param :: name : 日志名称
            @member :: clevel : 打印控制台级别
            @member :: Flevel : 输出日志文件级别

        '''
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

    def __init__(self, downloader=HtmlDownloader(), parser=HtmlParser(), requestManager=RequestManager(), writter=CommonWritter(), logger=None):
        logger = logger if logger is not None else Logger(
            self.__class__.__name__)
        super().__init__(downloader=downloader, parser=parser,
                         requestManager=requestManager, writter=writter, logger=logger)

    def write(self, filename):
        '''
        将数据写入磁盘，依赖于初始化Spider时的writter，默认为CommonWritter，即将数据打印到控制台
        '''
        self.writter.write(filename, None)

    def getItems(self):
        '''
        获取抓取到的数据
        '''
        return self.writter.items
