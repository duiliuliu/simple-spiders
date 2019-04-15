# -*- coding： utf-8 -*-
# author：pengr

from crawler.requestManager import RequestManager
import unittest


class test_RequestManager(unittest.TestCase):
    def setUp(self):
        self.manager = RequestManager()
        self.request = {
            'url': 'www.baidu.com',
            'request_type': 'post'
        }
        self.requests = self.generate_requests(4)

        self.requests_add_level = [self.request for i in range(20)]

    def generate_requests(self, num):
        requests = []
        for i in range(num):
            requests.append({
                'url': 'www.baidu.com?page={}'.format(i),
                'request_type': 'post'
            })
        return requests

    def test_add_new_request(self):
        self.manager.add_new_request(self.request)
        self.assertEqual(self.manager.new_requests_size(), 1)
        self.assertEqual(self.manager.new_requests_size(
            level=1), 1)

    def test_add_new_requests(self):
        self.manager.add_new_requests(self.requests)
        self.assertEqual(self.manager.new_requests_size(
            level=1), len(self.requests))
        self.assertEqual(self.manager.new_requests_size(), len(self.requests))

        self.manager.add_new_requests(self.requests)
        self.assertEqual(self.manager.new_requests_size(), len(self.requests))
        self.assertEqual(self.manager.new_requests_size(
            level=2), 0)

    def test_has_new_request(self):
        requests = self.generate_requests(5)
        self.manager.add_new_requests(requests)
        self.assertTrue(self.manager.has_new_request())
        self.assertTrue(self.manager.has_new_request(
            level=1))
        self.assertFalse(self.manager.has_new_request(
            level=2))

    def test_get_new_request(self):
        self.manager.add_new_request(self.request)
        self.assertEqual(self.manager.get_new_request(), self.request)

    def test_new_request_size(self):
        requests = self.generate_requests(5)
        self.manager.add_new_requests(requests)
        self.assertEqual(self.manager.new_requests_size(), len(requests))

    def test_old_request_size(self):
        requests = self.generate_requests(5)
        self.manager.add_new_requests(requests)
        self.assertEqual(self.manager.old_requests_size(), len(requests))
