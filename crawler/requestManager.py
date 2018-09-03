# -*- coding： utf-8 -*-
# author：pengr

import json
import hashlib


class RequestManager(object):

    def __init__(self, limit_level=3):
        self.__level = 0
        self.new_requests = {}
        self.old_requests = set()
        self.limit_level = limit_level

    def add_new_requests(self, requests, add_level=0):
        if not requests or len(requests) == 0:
            return
        for request in requests:
            self.add_new_request(request, add_level)

    def add_new_request(self, request, add_level=0):
        if not request:
            return
        request_str = json.dumps(request)
        if not request_str in self.old_requests:
            self.__add_new_request(request_str, add_level)
            self.__add_old_request(request_str)

    def __add_new_request(self, request_str, add_level=0):
        if not str(self.__level) in self.new_requests:
            self.new_requests[str(self.__level)] = set()

        if len(self.new_requests[str(self.__level)]) <= 0:
            self.__level += 1

        if self.__level+add_level > self.limit_level:
            return

        if not str(self.__level+add_level) in self.new_requests:
            self.new_requests[str(self.__level+add_level)] = set()
        self.new_requests[str(self.__level+add_level)].add(request_str)

    def __add_old_request(self, request_str):
        md5 = hashlib.md5()
        md5.update(request_str.encode('utf-8'))
        self.old_requests.add(md5.hexdigest()[8:-8])

    def has_new_request(self,):
        if self.new_request_size() > 0:
            return True
        return False

    def get_new_request(self,):
        if len(self.new_requests[str(self.__level)]) <= 0:
            self.__level += 1
        return json.loads(self.new_requests[str(self.__level)].pop())

    def new_request_size(self):
        if not str(self.__level+1) in self.new_requests:
            self.new_requests[str(self.__level+1)] = set()
        return len(self.new_requests[str(self.__level)])+len(self.new_requests[str(self.__level+1)])

    def old_request_size(self):
        return len(self.old_requests)
