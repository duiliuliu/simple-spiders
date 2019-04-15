# -*- coding: utf-8 -*-
# author: pengr

'''
sspider.api
~~~~~~~~~~~~

该模块提供一些常用功能函数

:copyright: (c) 2018 by pengr.
:license: GNU GENERAL PUBLIC LICENSE, see LICENSE for more details.
'''

from inspect import signature
import inspect
from functools import wraps
import codecs
import ctypes
import platform
import threading


def get__function_name():
    '''
    获取正在运行函数(或方法)名称
    '''
    return inspect.stack()[1][3]


def synchronized(func):
    '''
    锁（装饰器）
    '''
    func.__lock__ = threading.Lock()

    def lock_func(*args, **kwargs):
        with func.__lock__:
            return func(*args, **kwargs)
    return lock_func


'''
设置颜色
'''

FOREGROUND_WHITE = ''
FOREGROUND_BLUE = ''
FOREGROUND_GREEN = ''
FOREGROUND_RED = ''
FOREGROUND_YELLOW = ''

STD_OUTPUT_HANDLE = ''
std_out_handle = ''
if platform.system() == 'Windows':
    FOREGROUND_WHITE = 0x0007
    FOREGROUND_BLUE = 0x01
    FOREGROUND_GREEN = 0x0a
    FOREGROUND_RED = 0x0c
    FOREGROUND_YELLOW = FOREGROUND_RED | FOREGROUND_GREEN

    STD_OUTPUT_HANDLE = -11
    std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
elif platform.system() == 'Linux':
    FOREGROUND_WHITE = 0x0007
    FOREGROUND_BLUE = 0x01
    FOREGROUND_GREEN = '\033[1; 32m; {}\033[0m'
    FOREGROUND_RED = '\033[1;31m;{}\033[0m'
    FOREGROUND_YELLOW = '\033[1;33m;{}\033[0m'
else:
    pass


def set_color(color):
    '''
    设置颜色
    '''
    def wrapper(func):
        @wraps(func)
        def inner_wrapper(*args):
            if platform.system() == 'Windows':
                set_win_color(color)
                func(*args)
                set_win_color(FOREGROUND_WHITE)
            elif platform.system() == 'Linux':
                message = color.format(args[1])
                new_args = tuple([args[0], message])
                func(*new_args)
            else:
                func(*args)
            return
        return inner_wrapper
    return wrapper


def set_win_color(color, handle=std_out_handle):
    bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
    return bool


'''
类型检测
'''


def typeassert(*ty_args, **ty_kwargs):
    '''
    对函数进行类型检测
    '''
    def decorate(func):
        # If in optimized mode, disable type checking
        if not __debug__:
            return func

        # Map function argument names to supplied types
        sig = signature(func)
        bound_types = sig.bind_partial(*ty_args, **ty_kwargs).arguments

        @wraps(func)
        def wrapper(*args, **kwargs):
            bound_values = sig.bind(*args, **kwargs)
            # Enforce type assertions across supplied arguments
            for name, value in bound_values.arguments.items():
                if name in bound_types:
                    if not isinstance(value, bound_types[name]):
                        raise TypeError(
                            'Argument {} must be {}'.format(
                                name, bound_types[name])
                        )
            return func(*args, **kwargs)
        return wrapper
    return decorate


'''
判断字符编码
'''

# Null bytes; no need to recreate these on each call to guess_json_utf
_null = '\x00'.encode('ascii')  # encoding to ASCII for Python 3
_null2 = _null * 2
_null3 = _null * 3


def guess_utf(data):
    """
    :rtype: str
    """
    sample = data[:4]
    if sample in (codecs.BOM_UTF32_LE, codecs.BOM_UTF32_BE):
        return 'utf-32'     # BOM included
    if sample[:3] == codecs.BOM_UTF8:
        return 'utf-8-sig'  # BOM included, MS style (discouraged)
    if sample[:2] in (codecs.BOM_UTF16_LE, codecs.BOM_UTF16_BE):
        return 'utf-16'     # BOM included
    nullcount = sample.count(_null)
    if nullcount == 0:
        return 'utf-8'
    if nullcount == 2:
        if sample[::2] == _null2:   # 1st and 3rd are null
            return 'utf-16-be'
        if sample[1::2] == _null2:  # 2nd and 4th are null
            return 'utf-16-le'
        # Did not detect 2 valid UTF-16 ascii-range characters
    if nullcount == 3:
        if sample[:3] == _null3:
            return 'utf-32-be'
        if sample[1:] == _null3:
            return 'utf-32-le'
        # Did not detect a valid UTF-32 ascii-range character
    return None


def print_func(func):
    '''
    监测函数运行
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        print('- '*4+func.__name__+' running'+'- '*10)
        return func(*args, **kwargs)
    return wrapper
