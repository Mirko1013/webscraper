#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/4/17 9:10 AM
# @Author  : mirko
# @FileName: TextSelector.py
# @Software: PyCharm

from . import RegisterSelectorType, Selector


@RegisterSelectorType("SelectorText")
class TextSelector(Selector):



    def _getData(self):
        print("aaaa")
