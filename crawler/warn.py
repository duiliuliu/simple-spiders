# -*- coding： utf-8 -*-
# author：pengr


class Warn():
    '''
    警告
    警告对象，成员变量为警告message，__str__()返回message
    '''

    def __init__(self, message):
        '''
        警告初始化

            @member :: __message : 警告message

        '''
        self.__message = message

    def __str__(self):
        '''
        对象toString函数

            return message

        '''
        return self.__message
