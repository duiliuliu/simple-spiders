# -*- coding： utf-8 -*-
# author：pengr

from crawler.writter import DataWriter
import unittest


class test_DataWriter(unittest.TestCase):
 
        
    def test_write_txt(self):
        writter = DataWriter(filename='data.txt',type='txt')

    def test_write_csv(self):
        writter = DataWriter(filename='data.csv',type='csv')