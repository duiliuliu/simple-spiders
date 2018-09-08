# -*- coding： utf-8 -*-
# author：pengr

from crawler.htmlDownloader import HtmlDownloader
import unittest
from unittest import mock
import requests


class test_HtmlDownloader(unittest.TestCase):
    def setUp(self):
        self.downloader = HtmlDownloader()

    @mock.patch("requests.get")
    def test_download(self, mock_get):
        res = requests.Response()
        res.status_code = 200

        mock.Mock(res)

        mock_get.return_value = mock.Mock(return_value=res)
        request = {
            'url': 'www.baidu.com',
            'request_type': 'get',
            'level': '1'
        }

        self.assertDictEqual(self.downloader.download(request), {
            'url': 'www.baidu.com',
            'status': 200,
            'text': '文本',
            'level': '1'
        }, msg='with get type download occurs error!')

    def test_refresh_useragent(self):
        useragent = 'Mozilla/5.0 (Windows NT 10.0; WOW64)'
        self.downloader.refresh_useragent(useragent)
        self.assertEqual(self.downloader.headers['User-Agent'], useragent,
                         msg='refresh_proxy occurs error')

    def test_refresh_proxy(self):
        proxy = {
            'http': '10.10.26.253'
        }
        self.downloader.refresh_proxy(proxy)
        self.assertIn('http', self.downloader.proxy,
                      msg='refresh_proxy occurs error')

    def test_refresh_headers(self):
        headers = {
            'test': 'test'
        }
        self.downloader.refresh_headers(headers)
        self.assertIn('test', self.downloader.headers,
                      msg='refreah_headers occurs error!')

    def test_set_timeout(self):
        timeout = 10
        self.downloader.set_timeout(timeout)
        self.assertEqual(self.downloader.timeout,
                         timeout, msg='set_timeout occurs error!')

    def test_set_headers(self):
        headers = {
            'Accept': None
        }
        self.downloader.set_headers(headers)
        self.assertDictEqual(self.downloader.headers,
                             headers, msg='set_headers occurs error!')
