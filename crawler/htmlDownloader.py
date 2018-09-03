# -*- coding： utf-8 -*-
# author：pengr
import requests
import sys

from crawler.logger import Logger


class HtmlDownloader():
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.108 Safari/537.36 2345Explorer/8.8.0.16453'
        }
        self.proxy = {}
        self.timeout = 5
        self.logger = Logger(__name__)

    def download(self, request, data={}):
        if not request:
            return
        try:
            if request['request_type'] == 'post':
                response = self._post(request['url'], request['data'])
            else:
                response = self._get(request['url'])
        except:
            self.logger.exception('Requesting occurs error')

        if response.status_code == 200:
            response.encoding = 'utf-8'
            return response.text

        return response.status_code

    def _get(self, url):
        return requests.get(url, headers=self.headers, proxies=self.proxy, timeout=self.timeout)

    def _post(self, url, data):
        return requests.post(
            url, headers=self.headers, data=data, proxies=self.proxy, timeout=self.timeout)

    def refresh_useragent(self, useragent):
        if useragent:
            self.headers['User-Agent'] = useragent
        else:
            self.logger.exception('downloader refresh_useragent error')

    def refresh_proxy(self, proxy):
        if proxy and 'http' in proxy:
            self.proxy = proxy
        else:
            self.logger.exception('downloader refresh_proxy error')

    def refresh_headers(self, headers):
        for h in headers:
            if headers[h]:
                self.headers[h] = headers[h]
            else:
                self.headers.pop(h)

    def set_header(self, headers):
        if headers:
            self.headers = headers
