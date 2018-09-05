# -*- coding： utf-8 -*-
# author：pengr

from crawler.requestManager import RequestManager
import unittest


class requestManager_test(unittest.TestCase):
    def setUp(self):
        self.manager = RequestManager()
        self.request = {
            'url': 'ww.baidu.com',
            'request_type': 'post'
        }
        self.requests = [self.request for i in range(4)]
        self.requests_add_level = [self.request for i in range(20)]

    def test_add_new_request(self):
        self.manager.add_new_requests(self.requests)
        self.assertEqual(self.manager.new_request_size(), len(self.requests))
        self.assertEqual(self.manager.new_request_size(
            level=1), len(self.requests))

    def test_add_new_requests(self):
        self.manager = RequestManager()
        self.manager.add_new_requests(self.requests)
        self.assertEqual(self.manager.new_request_size(), len(self.requests))
        self.assertEqual(self.manager.new_request_size(
            level=1), len(self.requests))

        self.manager.add_new_requests(self.requests, add_level=1)
        self.assertEqual(self.manager.new_request_size(), len(self.requests)*2)
        self.assertEqual(self.manager.new_request_size(
            level=2), len(self.requests))

    def test_has_new_request(self):
        self.assertTrue(self.manager.has_new_request())
        self.assertTrue(self.manager.has_new_request(
            level=1))
        self.assertTrue(self.manager.has_new_request(
            level=2))
        self.assertFalse(self.manager.has_new_request(
            level=3))

    def test_get_new_request(self):
        self.assertEqual(self.manager.get_new_request(), self.request)

    def test_new_request_size(self):
        self.assertEqual(self.manager.new_request_size(
            level=2), len(self.requests))

    def test_old_request_size(self):
        self.assertEqual(self.manager.old_request_size(), len(self.requests)*2)

