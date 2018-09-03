# -*- coding = utf-8 -*-
# author：pengr

from crawler.htmlDownloader import HtmlDownloader
from crawler.htmlParser import HtmlParser
from crawler.requestManager import RequestManager
from crawler.logger import Logger
from crawler.writter import DataWrite
from crawler.warn import Warn
from multiprocessing.pool import Pool as ProcessPool
from multiprocessing.dummy import Pool as ThreadPool
import re


class Spider():

    instance = {}
    count = 0

    def __init__(self, start_request, name='spider', getUrl_func=None, getData_func=None, level=3):
        Spider.count += 1
        name += '-'+str(Spider.count)
        while name in Spider.instance:
            Spider.count += 1
        Spider.instance[name] = 1

        if type(start_request) == list:
            self.seed_url = '/'.join(start_request[0]['url'].split('/')[:-1])
        else:
            self.seed_url = '/'.join(start_request['url'].split('/')[:-1])
        self.start_request = start_request
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser(
            self.seed_url, getUrl_func=getUrl_func, getData_func=getData_func)
        self.requestManager = RequestManager(level)
        if type(start_request) == list:
            self.requestManager.add_new_requests(start_request)
        else:
            self.requestManager.add_new_request(start_request)
        self.logger = Logger(__name__)
        # self.sleep_time = 10

    def __call__(self, getUrl_func=None, getData_func=None):
        self.start_crawl()

    def start_crawl(self):
        self._start_icon()
        self.logger.info('\tStart crawl...')
        while self.requestManager.has_new_request():
            request = self.requestManager.get_new_request()
            self._crawl(request)
        self.logger.info('\tEnd crawl...')

    def start_multiProcess_crawl(self, capacity):
        self._start_icon()
        pool = ProcessPool(processes=capacity)
        while self.requestManager.has_new_request():
            request = self.requestManager.get_new_request()
            pool.apply_async(self._crawl, args=request)

        self.logger.info('\tWaiting for all subprocesses done...')
        pool.close()
        pool.join()
        self.logger.info('\tAll processes done!')
        DataWrite._writter_buffer_flush()

    def start_multiThread_crawl(self, capacity):
        self._start_icon()
        pool = ThreadPool(processes=capacity)
        while self.requestManager.has_new_request():
            request = self.requestManager.get_new_request()
            pool.apply_async(self._crawl, args=request)

        self.logger.info('\tWaiting for all subprocesses done...')
        pool.close()
        pool.join()
        self.logger.info('\tAll processes done!')
        DataWrite._writter_buffer_flush()

    def _crawl(self, request):
        self.logger.info('\t'+request['url'])
        try:
            content = self.downloader.download(request)
            if not re.match('\d{3}', str(content)):
                requests, data = self.parser.parse(content)
                if not (type(requests) == Warn):
                    self.requestManager.add_new_requests(requests, add_level=1)
                else:
                    self.logger.warn(
                        'parsed url error: ' + requests.__str__())
                if type(data) == Warn:
                    self.logger.warn(
                        'parsed data error: ' + data.__str__())
            else:
                self.logger.warn(
                    'crawled data is None and response_status is ' + str(content))

        except:
            self.logger.exception('\tCrawling occurs error')

    def _start_icon(self):
        with open('./crawler/banner.txt') as f:
            icon = f.read()
        print(icon)
        print()
