#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/4/17 9:07 AM
# @Author  : mirko
# @FileName: __init__.py.py
# @Software: PyCharm

import abc


class RegisterSelectorType(object):

    selector_type = {}

    def __init__(self, type):
        self._type = type

    def __call__(self, cls, *args, **kwargs):

        if not self.selector_type.__contains__(self._type):
            self.selector_type[self._type] = cls

        return cls


class SelectorFactory(object):

    __selector_type = RegisterSelectorType.selector_type

    @classmethod
    def create_selector(cls, type):

        if cls.__selector_type.__contains__(type):
            return cls.__selector_type[type]()
        else:
            raise NotImplementedError()


class Selector(object):


    __property = [
        "id", "type", "parentSelectors", "selector", "multiple", "regex", "delay"
    ]

    @classmethod
    def from_settings(cls, *args, **kwargs):
        sel = cls()
        sel.initInstance(*args, **kwargs)
        return sel


    def initInstance(self, *args, **kwargs):
        for key in kwargs.keys():
            if self.__property.__contains__(key):
                self.__setattr__(key, kwargs[key])
            else:
                raise TypeError("Attribute of the selector is illegal.")


    @abc.abstractmethod
    def _getData(self):
        raise NotImplementedError("Data extract function is not implemented.")










