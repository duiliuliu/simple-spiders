# -*- coding： utf-8 -*-
# author：pengr

from crawler.htmlParser import HtmlParser
import unittest


class test_HtmlParser(unittest.TestCase):
    def setUp(self):
        self.parser = HtmlParser('www.baidu.com')
        content = '''
                <html>
                <body>
                <ul>
                <li> <a href='/search?page=1'>第一页<a> </li>
                <li> <a href='/search?page=2'>第二页<a> </li>
                <li> <a href='/search?page=3'>第三页<a> </li>
                <li> <a href='/search?page=4'>第四页<a> </li>
                <li> <a href='/search?page=5'>第五页<a> </li>
                </ul>
                </body>
                </html>
                '''
        self.response = {
            'url': 'www.baidu.com',
            'status': 200,
            'text': content,
            'content': '',
            'level': 1
        }

    def test_parse(self):
        urls, data = self.parser.parse(self.response)
        self.assertEqual(len(urls), 5)
        self.assertDictEqual(urls[0], {'url': 'www.baidu.com/search?page=1'})
        self.assertEqual(data, None)

    def test_self_parse_url(self):
        pass

    def test_self_parse_data(self):
        pass
