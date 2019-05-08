# -*- coding = utf-8 -*-
# author：pengr

'''
sspider.抽象结构
~~~~~~~~~~~~

该模块时爬虫整体的抽象架构，可直接继承该模块中的类进行扩展功能
'''

from .utils import typeassert, get_function_name


class AbstractDownloader(object):

    '''
    下载器

    对传入的请求进行请求下载
    '''

    def download(self, request):
        '''
        对request进行请求下载，需要将请求到的response返回

            @param :: request : 请求对象
            return response
        '''
        raise NotImplementedError("未实现的父类方法: %s.%s" % (
            self.__class__.__name__, get_function_name()))


class AbstractParser(object):

    '''
    解析器

    对传入的文本进行解析
    '''

    def parse(self, response):
        '''
        对response进行解析，需要将解析到的requests与data返回

            @param :: response : 响应对象
            return requests,data
        '''
        raise NotImplementedError("未实现的父类方法: %s.%s" % (
            self.__class__.__name__, get_function_name()))


class AbstractRequestManager(object):

    '''
    请求管理器

    管理所有的请求
    '''

    def add_new_requests(self, requests):
        '''
        模板方法，不需要子类重写
        添加requests序列到requestManager中进行管理

            @param :: requests : request对象列表
            return None
        '''
        for request in requests:
            self.add_new_request(request)

    def add_new_request(self, request):
        '''
        添加request对象到requestManager中进行管理

            @param :: request : request对象
            return None
        '''
        raise NotImplementedError("未实现的父类方法: %s.%s" % (
            self.__class__.__name__, get_function_name()))

    def has_new_request(self):
        '''
        判断requestManager中是否还有新的请求，返回布尔类型结果

            return Bool
        '''
        raise NotImplementedError("未实现的父类方法: %s.%s" % (
            self.__class__.__name__, get_function_name()))

    def get_new_request(self):
        '''
        从requestManager中取新的请求

            return request
        '''
        raise NotImplementedError("未实现的父类方法: %s.%s" % (
            self.__class__.__name__, get_function_name()))


class AbstractWritter(object):

    '''
    数据写入类

    将数据以特定格式写入到磁盘中
    '''

    def write(self, data):
        '''
        将数据data写入磁盘

            return None
        '''
        raise NotImplementedError("未实现的父类方法: %s.%s" % (
            self.__class__.__name__, get_function_name()))

    def write_buffer(self, item):
        '''
        缓存数据

            return None
        '''
        raise NotImplementedError("未实现的父类方法: %s.%s" % (
            self.__class__.__name__, get_function_name()))

    def flush_buffer(self):
        '''
        刷新缓存数据到磁盘上

            return None
        '''
        raise NotImplementedError("未实现的父类方法: %s.%s" % (
            self.__class__.__name__, get_function_name()))


class AbstractLogger(object):

    '''
    日志类

    记录爬虫运行
    '''

    def debug(self, message):
        '''
        debug级别日志
        '''
        raise NotImplementedError("未实现的父类方法: %s.%s" % (
            self.__class__.__name__, get_function_name()))

    def info(self, message):
        '''
        info级别日志
        '''
        raise NotImplementedError("未实现的父类方法: %s.%s" % (
            self.__class__.__name__, get_function_name()))

    def warn(self, message):
        '''
        warn级别日志
        '''
        raise NotImplementedError("未实现的父类方法: %s.%s" % (
            self.__class__.__name__, get_function_name()))

    def exception(self, message):
        '''
        exception级别日志
        '''
        raise NotImplementedError("未实现的父类方法: %s.%s" % (
            self.__class__.__name__, get_function_name()))

    def error(self, message):
        '''
        error级别日志
        '''
        raise NotImplementedError("未实现的父类方法: %s.%s" % (
            self.__class__.__name__, get_function_name()))


class AbstractSpider(object):
    '''
    爬取调度器

        @member :: downloader : 下载器
        @member :: parser : 解析器
        @member :: requestManager : 请求管理器
        @member :: writter : 文本写入
        @member :: logger : 日志

    '''
    attrs = [
        'downloader', 'parser', 'requestManager', 'writter', 'logger'
    ]

    @typeassert(downloader=AbstractDownloader, parser=AbstractParser, requestManager=AbstractRequestManager, writter=AbstractWritter, logger=AbstractLogger)
    def __init__(self, downloader=AbstractDownloader(), parser=AbstractParser(), requestManager=AbstractRequestManager(), writter=AbstractWritter(), logger=AbstractLogger()):
        self.downloader = downloader
        self.parser = parser
        self.requestManager = requestManager
        self.writter = writter
        self.logger = logger

    def __call__(self, request):
        self.run(request)

    def run(self, requests):
        '''
        运行爬虫方法，从requestManager中取出可用的request，然后扔进下载器中进行下载，通过解析器对下载到的文档进行解析；
        需要传入一个或者一组request作为初始request进行抓取

            @param :: request : 请求
            return : None
        '''
        self.__start_icon()
        self.logger.info('\tStart crawl...')
        if  isinstance (requests,list) :
            self.requestManager.add_new_requests(requests)
        else:
            self.requestManager.add_new_request(requests)
        while self.requestManager.has_new_request():
            request = self.requestManager.get_new_request()
            self.crawl(request)
        self.logger.info('\tEnd crawl...')

    def crawl(self, request):
        '''
        对request进行请求进行爬取并解析结果的运行单元，子类可对该方法重写进行多线程、多进程运行或异步抓取与解析
        下载器对传入的request进行下载，解析器解析下载到的文档，并将解析出的request扔进requestManager中进行管理，以进行深度爬取；将解析出的data扔进writter中，将数据存储到磁盘上

            @param :: requests : 请求 or 请求集合
            return None
        '''
        try:
            self.logger.info('\t'+request.url)
            response = self.downloader.download(request)
            requests, data = self.parser.parse(response)
            self.requestManager.add_new_requests(requests)
            self.writter.write_buffer(data)
        except Exception as e:
            self.logger.exception('\tCrawling occurs error\n' + e.__repr__())

    def write(self):
        '''
        传入文件名及格式，数据写入文件
        '''
        self.writter.flush_buffer()

    def __start_icon(self):
        icon = '''
     _              _       ___       _    _           
 ___<_>._ _ _  ___ | | ___ / __> ___ <_> _| | ___  _ _ 
<_-<| || ' ' || . \| |/ ._>\__ \| . \| |/ . |/ ._>| '_>
/__/|_||_|_|_||  _/|_|\___.<___/|  _/|_|\___|\___.|_|  
              |_|               |_|                    

            '''
        print(icon)
        print()
