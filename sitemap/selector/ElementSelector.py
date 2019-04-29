#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/4/17 9:09 AM
# @Author  : mirko
# @FileName: ElementSelector.py
# @Software: PyCharm

from . import RegisterSelectorType, Selector


@RegisterSelectorType("SelectorElement")
class ElementSelector(Selector):

    def _getData(self):
        print("aaaa")
