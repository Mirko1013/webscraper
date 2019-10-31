#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/10/31 9:17 PM
# @Author  : mirko
# @FileName: ClickSelector.py
# @Software: PyCharm

from . import RegisterSelectorType, Selector
from pyquery import PyQuery as pq

@RegisterSelectorType("SelectorClick")
class ClickSelector(Selector):

    can_return_multiple_records = False
    can_have_child_selectors = True
    can_have_local_child_selectors = True
    can_create_new_jobs = True
    can_return_elements = False

    features = {
        'multiple': False,
        'delay': 0
    }

    def __int__(self, id, type, css_paths, parent_selectors, multiple, delay, **kwargs):
        super(ClickSelector, self).__init__(id, type, css_paths, parent_selectors)
        self.multiple = multiple
        self.delay = delay

    @classmethod
    def get_features(cls):
        base_features = Selector.get_features()
        base_features.update(cls.features)

        return base_features
    def will_return_multiple_records(self):
        return self.multiple and self.can_return_multiple_records

    def get_specific_data(self, element):
        pass