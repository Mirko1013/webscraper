#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/11/1 14:23
# @Author  : mirko
# @FileName: Utils.py
# @Software: PyCharm

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