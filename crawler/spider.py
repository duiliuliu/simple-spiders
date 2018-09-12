# -*- coding = utf-8 -*-
# author：pengr

from crawler.htmlDownloader import HtmlDownloader
from crawler.htmlParser import HtmlParser
from crawler.requestManager import RequestManager
from crawler.logger import Logger
from crawler.writter import DataWriter
from crawler.warn import Warn
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, wait
import time


class Spider():
    '''
    爬取调度器
    初始化需传入一个start_request
    '''

    instance = {}
    count = 0

    def __init__(self, start_request, name='spider', getUrl_func=None, getData_func=None, level=3):
        Spider.count += 1
        name += '-'+str(Spider.count)
        while name in Spider.instance:
            Spider.count += 1
        Spider.instance[name] = 1

        if type(start_request) == list:
            self._seed_url = '/'.join(start_request[0]['url'].split('/')[:-1])
        elif type(start_request) == dict:
            self._seed_url = '/'.join(start_request['url'].split('/')[:-1])
            start_request = [start_request]
        else:
            self._seed_url = '/'.join(start_request.split('/')[:-1])
            start_request = [{'url': start_request}]

        self._start_request = start_request
        self._downloader = HtmlDownloader()
        self._parser = HtmlParser(
            self._seed_url, getUrl_func=getUrl_func, getData_func=getData_func)
        self._requestManager = RequestManager(level)
        self._requestManager.add_new_requests(start_request)
        self._logger = Logger(__name__)
        # self.sleep_time = 10

    def __call__(self, type=None):
        self.start_crawl()

    def start_crawl(self):
        '''
        爬取方法，对requestManager中的url进行请求downloa，然后解析。

            return : None
        '''
        self._start_icon()
        self._logger.info('\tStart crawl...')
        while self._requestManager.has_new_request():
            request = self._requestManager.get_new_request()
            self._crawl(request)
        self._logger.info('\tEnd crawl...')
        DataWriter._writter_buffer_flush()

    def start_multiProcess_crawl(self, capacity):
        '''
        多进程爬取方法，对requestManager中的url进行请求downloa，然后解析。

            @param :: capacity : 进程池容量

            return : None
        '''
        self._start_icon()
        self._logger.info('\tStart multiProcess_crawl...')
        pool = ProcessPoolExecutor(capacity)
        futures = []
        # import pdb;pdb.set_trace()
        while self._requestManager.has_new_request():
            level = self._requestManager.get_level()
            while self._requestManager.has_new_request(level):
                request = self._requestManager.get_new_request(level)
                futures.append(pool.submit(self._crawl, request))
                self._logger.info(
                    '\tWaiting level-{} subprocesses done...'.format(level))
            wait(futures)
            # wait(futures, timeout=None, return_when='FIRST_COMPLETED')
        self._logger.info('\tAll subprocesses done!')
        DataWriter._writter_buffer_flush()

    def start_multiThread_crawl(self, capacity):
        '''
        多线程爬取方法，对requestManager中的url进行请求downloa，然后解析。

            @param :: capacity : 线程池容量

            return : None
        '''
        self._start_icon()
        self._logger.info('\tStart multiProcess_crawl...')
        pool = ThreadPoolExecutor(capacity)
        futures = []
        # import pdb;pdb.set_trace()
        while self._requestManager.has_new_request():
            level = self._requestManager.get_level() 
            while self._requestManager.has_new_request(level):
                request = self._requestManager.get_new_request(level)
                futures.append(pool.submit(self._crawl, request))
                self._logger.info(
                    '\tWaiting level-{} subthreads done...'.format(level))
            wait(futures)
            # wait(futures, timeout=None, return_when='FIRST_COMPLETED')
        self._logger.info('\tAll subthreads done!')
        DataWriter._writter_buffer_flush()

    def _crawl(self, request):
        if not request:
            return
        try:
            self._logger.info('\t'+request['url'])
            response = self._downloader.download(request)
            if response['status'] == 200:
                requests, data = self._parser.parse(response)
                if not (type(requests) == Warn):
                    self._requestManager.add_new_requests(requests)
                else:
                    self._logger.warn(
                        'parsed url error: ' + requests.__str__())
                if type(data) == Warn:
                    self._logger.warn(
                        'parsed data error: ' + data.__str__())
            else:
                self._logger.warn(
                    'crawled data is None and response_status is ' + str(response['status']))
        except:
            self._logger.exception('\tCrawling occurs error')

    def _start_icon(self):
        icon = '''
      _                 _         _____       _     _           
     (_)               | |       / ____|     (_)   | |          
  ___ _ _ __ ___  _ __ | | ___  | (___  _ __  _  __| | ___ _ __ 
 / __| | '_ ` _ \| '_ \| |/ _ \  \___ \| '_ \| |/ _` |/ _ \ '__|
 \__ \ | | | | | | |_) | |  __/  ____) | |_) | | (_| |  __/ |   
 |___/_|_| |_| |_| .__/|_|\___| |_____/| .__/|_|\__,_|\___|_|   
                 | |                   | |                      
                 |_|                   |_|                      
            '''
        print(icon)
        print()
