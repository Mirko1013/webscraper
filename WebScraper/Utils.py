#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/11/1 14:23
# @Author  : mirko
# @FileName: Utils.py
# @Software: PyCharm


import time, threading
import hashlib
from w3lib.url import canonicalize_url

DICT_OR_SINGLE_VALUES = (dict, bytes)

def arg2iter(arguments):
    """
        将入参转化为严格意义上的可迭代list对象
    """
    if not arguments:
        return []
    elif not isinstance(arguments, DICT_OR_SINGLE_VALUES) and hasattr(arguments, '__iter__'):
        return arguments
    else:
        return [arguments]


def get_md5(str):
    return hashlib.md5(to_bytes(str)).hexdigest()


def to_bytes(str, encoding=None):
    if isinstance(str, bytes):
        return str
    if not encoding:
        encoding = "utf-8"

    return str.encode(encoding)



class setInterval(object):
    def __init__(self, interval, func, *args, **kwargs):
        self.interval = interval
        self.func = func
        self.stop_event = threading.Event()
        #传入stop_event，适配于闭包函数
        thread = threading.Thread(target=self.__task_func, args=(self.stop_event, *args), kwargs=kwargs)
        thread.start()

        #使主线程进入阻塞
        thread.join()


    def __task_func(self, *args, **kwargs):
        """
        利用threading event的特性，wait(timeout)会阻塞当前进程，超时后会继续
        调用set()方法后event会返回true，继而退出循环，结束setInterval调用
        :param args:
        :param kwargs:
        :return:
        """

        next_time = time.time() + self.interval
        while not self.stop_event.wait(next_time - time.time()):
            next_time += self.interval
            self.func(*args, **kwargs)

    def cancel(self):
        self.stop_event.set()

def request_fingerprint(url):
    fp = hashlib.sha1()
    fp.update(to_bytes(canonicalize_url(url=url)))

    return fp.hexdigest()
