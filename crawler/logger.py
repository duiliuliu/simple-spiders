# -*- coding： utf-8 -*-
# author：pengr
import logging
import os
import ctypes
import platform
import threading

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

def synchronized(func):
    func.__lock__ = threading.Lock()

    def lock_func(*args, **kwargs):
        with func.__lock__:
            return func(*args, **kwargs)
    return lock_func

@synchronized
def set_color(color):
    def wrapper(func):
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


class Logger:

    def __init__(self, name, clevel=logging.DEBUG, Flevel=logging.DEBUG):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        fmt = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')
        # 设置CMD日志
        sh = logging.StreamHandler()
        sh.setFormatter(fmt)
        sh.setLevel(clevel)
        # 设置文件日志
        # fh = logging.FileHandler(path)
        # fh.setFormatter(fmt)
        # fh.setLevel(Flevel)
        self.logger.addHandler(sh)
        # self.logger.addHandler(fh)

    def debug(self, message):
        self.logger.debug(message)

    @set_color(FOREGROUND_GREEN)
    def info(self, message):
        self.logger.info(message)

    @set_color(FOREGROUND_YELLOW)
    def warn(self, message):
        self.logger.warn(message)

    @set_color(FOREGROUND_RED)
    def exception(self, message):
        self.logger.exception(message)

    @set_color(FOREGROUND_RED)
    def error(self, message):
        self.logger.error(message)

    def cri(self, message):
        self.logger.critical(message)
