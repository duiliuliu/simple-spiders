# -*- coding： utf-8 -*-
# author：pengr
import os
import sys
import threading
import xlsxwriter
import csv
from xlwt import Workbook

from crawler.logger import Logger


def synchronized(func):
    func.__lock__ = threading.Lock()

    def lock_func(*args, **kwargs):
        with func.__lock__:
            return func(*args, **kwargs)

    return lock_func


class DataWrite():

    instance = {}

    @synchronized
    def __new__(cls, *args, **kwargs):
        if args:
            filename = args[0]
        else:
            filename = kwargs['filename']
        if not filename in cls.instance:
            cls.instance[filename] = super().__new__(cls)
        return cls.instance[filename]

    def __init__(self, filename, **kwargs):
        if not os.path.exists('./source'):
            os.mkdir('./source')
        self.filename = filename
        self.headers = []
        if filename.split('.')[-1]:
            self.type = filename.split('.')[-1]
        else:
            self.type = 'txt'
        self.encoding = 'utf-8'
        self.write_type = 'a'
        self.__attribute = {}
        self.__data = []
        self.logger = Logger(__name__)

        for k, v in kwargs.items():
            setattr(self, k, v)

    @staticmethod
    def _writter_buffer_flush():
        for name in DataWrite.instance:
            writter = DataWrite.instance[name]
            writter.flush_buffer()

    def write(self, items=None):
        if self.type == 'txt':
            self._write_txt(items)
        elif self.type == 'csv':
            self._write_csv(items)
        elif self.type == 'xexcel':
            self._write_xexcel(items)
        elif self.type == 'excel':
            self._write_excel(items)
        else:
            self.logger.exception("Illegal file-type defined")

    def write_buffer(self, item, flush_num=1000):
        if not item:
            return
        if type(item) == dict:
            item = self._dict_to_list(item)
        self.__data.append(item)
        if len(self.__data) > flush_num:
            self.flush_buffer()

    # @staticmethod
    def has_buffer(self):
        return len(self.__data) > 0

    def flush_buffer(self):
        if len(self.__data) > 0:
            self.write(self.__data)
            del self.__data[:]

    def _write_txt(self, items):
        with open(self.filename, self.write_type, encoding=self.encoding) as f:
            if self.headers and (self.filename not in self.__attribute):
                item = self.headers
                if type(self.headers) == dict:
                    item = self._dict_to_list(self.headers)
                f.write('\t'.join(item)+'\n')
                f.write('-'*40+'\n')
                self.__attribute[self.filename] = '1'

            for item in items:
                if type(item) == dict:
                    item = self._dict_to_list(item)
                f.write('\t'.join(item)+'\n')

    def _write_excel(self, items):
        book = Workbook()
        worksheet = book.add_sheet("Sheet 1")
        row = 0
        col = 0
        if self.headers and (self.filename not in self.__attribute):
            item = self.headers
            if type(self.headers) == dict:
                item = self._dict_to_list(self.headers)
            for h in item:
                worksheet.write.write(row, col, h)
                col += 1
            row += 1
            col = 0
            self.__attribute[self.filename] = '1'

        for item in items:
            if type(item) == dict:
                item = self._dict_to_list(item)
            for i in item:
                worksheet.write(row, col, i)
                col += 1
            row += 1
            col = 0
            if row > 65535:
                print(
                    "\033[31mHit limit of #of rows in one sheet(65535).\033[0m", file=sys.stderr)
                break
        book.save(self.filename)

    def _write_xexcel(self, items):
        workbook = xlsxwriter.Workbook(self.filename)
        worksheet = workbook.add_worksheet()
        row = 0
        col = 0
        if self.headers and (self.filename not in self.__attribute):
            item = self.headers
            if type(self.headers) == dict:
                item = self._dict_to_list(self.headers)
            for h in item:
                worksheet.write(row, col, h)
                col += 1
            row += 1
            col = 0
            self.__attribute[self.filename] = '1'

        for item in items:
            if type(item) == dict:
                item = self._dict_to_list(item)
            for i in item:
                worksheet.write(row, col, i)
                col += 1
            row += 1
            col = 0

        workbook.close()

    def _write_csv(self, items):
        with open(self.filename, self.write_type, newline='', encoding=self.encoding) as f:
            csvfile = csv.writer(f)
            if self.headers and (self.filename not in self.__attribute):
                item = self.headers
                if type(self.headers) == dict:
                    item = self._dict_to_list(self.headers)
                csvfile.writerow(item)
                self.__attribute[self.filename] = '1'

            for item in items:
                if type(item) == dict:
                    item = self._dict_to_list(item)
                csvfile.writerow(item)

    def _dict_to_list(self, items_dict):
        try:
            items = []
            if not self.headers:
                self.header = list(items_dict.keys())

            for key in self.headers:
                try:
                    items.append(items_dict[key])
                except:
                    items.append('')

            return items
        except Exception as e:
            self.logger.exception('please set ture headers in writter!\n')
