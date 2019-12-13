#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/11/1 11:35
# @Author  : mirko
# @FileName: __init__.py.py
# @Software: PyCharm


class RegisterProcessorType(object):

    processor_type = {}

    def __init__(self, type):
        self._type = type

    def __call__(self, cls, *args, **kwargs):
        if not self.processor_type.__contains__(self._type):
            self.processor_type[self._type] = cls

        return cls


class ProcessorFactory(object):
    __processor_type = RegisterProcessorType.processor_type

    @classmethod
    def create_processor(cls, type):
        if cls.__processor_type.__contains__(type):
            return cls.__processor_type[type]
        else:
            raise NotImplementedError()

class Processor(object):

    def __init__(self):
        self.pre_check()

    def __call__(self, data, *args, **kwargs):
        return self.do_process(data)


    def get_settings(self):
        raise NotImplementedError()

    @classmethod
    def from_settings(cls, *settings):
        return cls(*settings)

    def do_process(self, data, *args, **kwargs):
        """
        对外暴露do_process接口
        :param args:
        :param kwargs:
        :return:
        """
        raise NotImplementedError()

    def pre_check(self):
        raise NotImplementedError()