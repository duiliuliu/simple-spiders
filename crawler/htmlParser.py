# -*- coding： utf-8 -*-
# author：pengr
from lxml import html
from crawler.warn import Warn


class HtmlParser():

    def __init__(self, seed_url, getUrl_func=None, getData_func=None):
        self.seed_url = seed_url
        self.getUrl_func = getUrl_func
        self.getData_func = getData_func

    def parse(self, content):
        return self._getUrl(content), self._getData(content)

    def _getUrl(self, content):
        if self.getUrl_func:
            try:
                return self.getUrl_func(content)
            except Exception as e:
                return Warn(repr(e))
        content = html.fromstring(content)
        return {'url': self.seed_url+link for link in content.xpath('//a/@href')}

    def _getData(self, content):
        if self.getData_func:
            try:
                return self.getData_func(content)
            except Exception as e:
                return Warn(repr(e))
        print(content)
        return None
