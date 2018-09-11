import sys
import os
sys.path.insert(0,os.path.abspath('..'))

from crawler.writter import DataWriter

writter = DataWriter('data',type='csv')
writter.write([[1,2,3,4]])