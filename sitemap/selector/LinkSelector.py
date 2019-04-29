#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/4/22 9:20 PM
# @Author  : mirko
# @FileName: LinkSelector.py
# @Software: PyCharm

from . import RegisterSelectorType, Selector


@RegisterSelectorType("LinkSelector")
class LinkSelector(Selector):

    def _getData(self):
        print("aaaa")

