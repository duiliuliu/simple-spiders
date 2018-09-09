# -*- coding： utf-8 -*-
# author：pengr
import requests
import sys


class HtmlDownloader():
    '''
    资源下载器
    进行网络请求资源，返回utf-8格式的文本

    '''

    def __init__(self):
        '''
        资源下载器初始化函数

            @member :: __headers : 请求头，默认设置useAgent属性
            @member :: __proxy : 请求代理，默认None
            @member :: __timeout : 请求延时设置，默认延时5秒
            @member :: __level : 当前请求层数，对应不同的层数可以有不同的设置

        '''
        self.__headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.108 Safari/537.36 2345Explorer/8.8.0.16453'
        }
        self.__proxy = {}
        self.__timeout = 5
        self.__level = 0

    def download(self, request):
        '''
        资源下载，返回一个response字典，属性有status:响应状态码；text: 响应内容；url:请求url；level：当前请求的网络层数

            @param :: request : 打算访问的请求

            return : Response

        '''
        if not request:
            return {
                'status': '空请求',
                'url': '',
                'text': '',
                'content': '',
                'level': ''
            }

        self.__level = request['level']

        try:
            if 'request_type' in request and request['request_type'] == 'post':
                data = request['data'] if 'data' in request else None
                response = self._post(request['url'], data)
            else:
                response = self._get(request['url'])
        except:
            raise Exception('downloding occurs error')

        response.encoding = 'utf-8'
        return {
            'url': request['url'],
            'status': response.status_code,
            'text': response.text,
            'content': response.content,
            'level': request['level']
        }

    def refresh_useragent(self, useragent):
        '''
        更新浏览器头

            @param :: useragent : 打算更新的浏览器头

            return : None

        '''
        if useragent:
            self.__headers['User-Agent'] = useragent

    def refresh_proxy(self, proxy):
        '''
        更新请求代理，打算更新的请求代理为一个字典，应有键'http'

            @param :: proxy : 打算更新的代理

            return : None

        '''
        if proxy and 'http' in proxy:
            self.__proxy = proxy

    def refresh_headers(self, headers, level=None):
        '''
        更新请求头，传入的请求头字典中，值为None表示请求头更新剔除相应的键，值不为None则更新相应的值

            @param :: headers : 打算更新的请求头

            @param :: level : 为相应的网络层级更新请求头，默认为None，即立即更新请求头

            return : None

        '''
        if not headers:
            return
        if not level or level == self.__level:
            for h in headers:
                if headers[h]:
                    self.__headers[h] = headers[h]
                else:
                    self.__headers.pop(h)

    def set_timeout(self, timeout):
        '''
        设置延时

            @param :: timeout : 打算设置的延时

            return : None

        '''
        if timeout:
            self.__timeout = timeout

    def set_headers(self, headers, level=None):
        '''
        设置请求头，直接以传入的请求头作为请求头

            @param :: headers : 打算设置的请求头

            @param :: level : 相应的网络层级设置请求头，默认为None，即立即设置请求头

            return : None

        '''
        if not headers:
            return
        if not level or level == self.__level:
            self.__headers = headers

    def _get(self, url):
        '''
        (私有函数)get请求,引用requests库进行get请求，返回一个Response对象

            @param :: url : 打算请求的url

            return : <Response>

        '''
        return requests.get(url, headers=self.__headers, proxies=self.__proxy, timeout=self.__timeout)

    def _post(self, url, data):
        '''
        (私有函数)post请求，引用requests库进行post请求，返回一个Response对象

            @param :: url : 打算请求的url

            @param :: data : post请求的数据主体

            return : <Response>

        '''
        return requests.post(
            url, headers=self.__headers, data=data, proxies=self.__proxy, timeout=self.__timeout)
