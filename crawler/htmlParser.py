# -*- coding： utf-8 -*-
# author：pengr
from lxml import html
from crawler.warn import Warn


class HtmlParser():
    '''
    网页解析器
    默认使用lxml进行解析，可自定义url提取方式与数据提取方式，将自定义解析函数作为对象传入解析器进行解析
    '''

    def __init__(self, seed_url, getUrl_func=None, getData_func=None):
        '''
        网页解析器初始化函数

            @member :: __seed_url : 种子url，所有解析到的url与seed_url进行拼接，构成完整url
            @member :: __getUrl_func : 自定义解析url函数
            @member :: __getData_func : 自定义解析数据函数

        '''
        self.__seed_url = seed_url
        self.__getUrl_func = getUrl_func
        self.__getData_func = getData_func

    def parse(self, response):
        '''
        解析函数、返回url集合与数据集合

            @param :: response : 打算解析响应内容，是一个字典，包含属性 'url','status','text','content','level',分别表示请求url，响应状态码，响应文本，响应内容 (二进制),请求层级

            return : list<url>、list<data>

        '''
        return self._getUrl(response), self._getData(response)

    def _getUrl(self, response):
        '''
        (私有函数)url解析函数，用户有自定义实现则以用户自定义实现为主

            @param :: response : 打算解析的文本

            return : list<url>

        '''
        if self.__getUrl_func:
            try:
                return self.__getUrl_func(response)
            except Exception as e:
                return Warn(repr(e))
        content = html.fromstring(response['text'])
        return [{'url': self.__seed_url+link} for link in content.xpath('//a/@href')]

    def _getData(self, response):
        '''
        (私有函数)data解析函数，用户有自定义实现则以用户自定义实现为主

            @param :: response : 打算解析的文本

            return : list<data>

        '''
        if self.__getData_func:
            try:
                return self.__getData_func(response)
            except Exception as e:
                return Warn(repr(e))
        print(response['text'])
        return None
