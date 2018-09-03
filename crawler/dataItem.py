# -*- coding： utf-8 -*-
# author：pengr
import threading


def synchronized(func):
    func.__lock__ = threading.Lock()

    def lock_func(*args, **kwargs):
        with func.__lock__:
            return func(*args, **kwargs)

    return lock_func


class DataItem(object):

    instance = None
    itemField = {}

    @synchronized
    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self, *args ,**kwargs):
        for i in args:
            self.itemField[i] = ''
        
        for k,v in kwargs:
            self.itemField[k] = v

    def setField(self, name):
        self.itemField[name] = ''
