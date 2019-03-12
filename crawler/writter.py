# -*- coding： utf-8 -*-
# author：pengr
import os
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


class DataWriter():
    '''
    数据写入类
    支持多种数据格式写入文本，初始化类实例时，可传入一个字典格式的headers,key作为所有数据的key,value作为数据写入后的头部

            @param :: filename : 数据写入文件名

            @member :: headers : 数据写入文件头部

            @member :: type : 数据写入文件格式，默认txt

            @member :: encoding : 数据写入文件编码，默认utf-8

            @member :: write_type : 数据写入文件方式，默认'a'
    '''

    instance = {}

    @synchronized
    def __new__(cls, *args, **kwargs):
        '''
        数据写入构造器，按照文件名构造写入类，相同的文件名返回同一个实例

            @member :: instance : 存贮实例集合

        '''
        if args:
            filename = args[0]
        else:
            filename = kwargs['filename']
        if not filename in cls.instance:
            cls.instance[filename] = super().__new__(cls)
        return cls.instance[filename]

    def __init__(self, filename, **kwargs):
        '''
        请求管理器初始化函数

            @param :: filename : 数据写入文件名

            @member :: headers : 数据写入文件头部

            @member :: type : 数据写入文件格式，默认txt

            @member :: encoding : 数据写入文件编码，默认utf-8

            @member :: write_type : 数据写入文件方式，默认'a'

            @member :: logger : 日志
        '''
        
        
        self.__filename = filename
        self._headers = []
        self.type = filename.split('.')[-1] if len(filename.split('.')) > 1 else ''
        self._encoding = 'utf-8'
        self._write_type = 'w'
        self.__attribute = {}
        self.__data = []
        self.__logger = Logger(__name__)

        for k, v in kwargs.items():
            self.__setattr__(k, v)

    @staticmethod
    def _writter_buffer_flush():
        '''
        类方法，刷新文件内容

            @param :: filename : 打算刷新的文件名称

            return : None
        '''
        for name in DataWriter.instance:
            writter = DataWriter.instance[name]
            writter.flush_buffer()

    def write(self, items=None):
        '''
        文件写入，写入数据格式为二维结构，即二维列表或者二维字典，或者相互组合

            @param :: items : 数据序列

            return : None
        '''
        if self.type == 'txt':
            self._write_txt(items)
        elif self.type == 'csv':
            self._write_csv(items)
        elif self.type == 'xexcel':
            self._write_xexcel(items)
        elif self.type == 'excel':
            self._write_excel(items)
        else:
            self.__logger.exception("Illegal file-type defined")

    def write_buffer(self, item, flush_num=1000):
        '''
        文件以缓冲方式写入，写入数据格式为二维结构，即二维列表或者二维字典，或者相互组合

            @param :: items : 数据序列

            return : None
        '''
        self._write_type = 'a'
        if not item:
            return
        self._add_buffer_data(item)
        if len(self.__data) > flush_num:
            self.flush_buffer()

    # @staticmethod
    def has_buffer(self):
        '''
        缓冲区是否有数据

            return : Bool
        '''
        return len(self.__data) > 0

    def flush_buffer(self):
        '''
        刷新缓冲

            return : None
        '''
        if self.has_buffer():
            self.write(self.__data)
            del self.__data[:]

    def _write_txt(self, items):
        '''
        (私有函数)txt格式写入，写入数据格式为二维结构，即二维列表或者二维字典，或者相互组合

            @param :: items : 数据序列

            return : None
        '''
        with open(self.__filename, self._write_type, encoding=self._encoding) as f:
            if self._headers and (self.__filename not in self.__attribute):
                item = self._headers
                if type(self._headers) == dict:
                    item = self._dict_to_list(self._headers)
                f.write('\t'.join(str(i) for i in item)+'\n')
                f.write('-'*40+'\n')
                self.__attribute[self.__filename] = '1'

            for item in items:
                if type(item) == dict:
                    item = self._dict_to_list(item)
                f.write('\t'.join(str(i) for i in item)+'\n')

    def _write_excel(self, items):
        '''
        (私有函数)xls格式写入，写入数据格式为二维结构，即二维列表或者二维字典，或者相互组合

            @param :: items : 数据序列

            return : None
        '''
        book = Workbook()
        worksheet = book.add_sheet("Sheet 1")
        row = 0
        col = 0
        if self._headers and (self.__filename not in self.__attribute):
            item = self._headers
            if type(self._headers) == dict:
                item = self._dict_to_list(self._headers)
            for h in item:
                worksheet.write.write(row, col, h)
                col += 1
            row += 1
            col = 0
            self.__attribute[self.__filename] = '1'

        for item in items:
            if type(item) == dict:
                item = self._dict_to_list(item)
            for i in item:
                worksheet.write(row, col, i)
                col += 1
            row += 1
            col = 0
            if row > 65535:
                self.__logger.warn(
                    "Hit limit of #of rows in one sheet(65535).")
                break
        book.save(self.__filename)

    def _write_xexcel(self, items):
        '''
        (私有函数)xlsx格式写入，写入数据格式为二维结构，即二维列表或者二维字典，或者相互组合

            @param :: items : 数据序列

            return : None
        '''
        workbook = xlsxwriter.Workbook(self.__filename)
        worksheet = workbook.add_worksheet()
        row = 0
        col = 0
        if self._headers and (self.__filename not in self.__attribute):
            item = self._headers
            if type(self._headers) == dict:
                item = self._dict_to_list(self._headers)
            for h in item:
                worksheet.write(row, col, h)
                col += 1
            row += 1
            col = 0
            self.__attribute[self.__filename] = '1'

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
        '''
        (私有函数)csv格式写入，写入数据格式为二维结构，即二维列表或者二维字典，或者相互组合

            @param :: items : 数据序列

            return : None
        '''
        with open(self.__filename, self._write_type, newline='', encoding=self._encoding) as f:
            csvfile = csv.writer(f)
            if self._headers and (self.__filename not in self.__attribute):
                item = self._headers
                if type(self._headers) == dict:
                    item = self._dict_to_list(self._headers)
                csvfile.writerow(item)
                self.__attribute[self.__filename] = '1'

            for item in items:
                if type(item) == dict:
                    item = self._dict_to_list(item)
                csvfile.writerow(item)

    @synchronized
    def _add_buffer_data(self, item):
        if type(item) == dict:
            item = self._dict_to_list(item)
        self.__data.extend(item)

    def _dict_to_list(self, items_dict):
        '''
        (私有函数)字典转换列表，以文件头部为基准

            @param :: items_dict : 打算转换的列表

            return : None
        '''
        try:
            items = []
            if not self._headers:
                self.header = list(items_dict.keys())

            for key in self._headers:
                try:
                    items.append(items_dict[key])
                except:
                    items.append('')

            return items
        except Exception as e:
            self.__logger.exception('please set true headers in writter!')
