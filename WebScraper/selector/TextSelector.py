#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/4/17 9:10 AM
# @Author  : mirko
# @FileName: TextSelector.py
# @Software: PyCharm

from . import RegisterSelectorType, Selector
from pyquery import PyQuery as pq

@RegisterSelectorType("SelectorText")
class TextSelector(Selector):

    can_return_multiple_records = True
    can_have_child_selectors = False
    can_have_local_child_selectors = False
    can_create_new_jobs = False
    can_return_elements = False

    features = {
        'multiple': False,
        'delay': 0,
        'regex': ''
    }

    def __init__(self, id, type, css_paths, parent_selectors, multiple, delay, regex, **kwargs):
        super(TextSelector, self).__init__(id, type, css_paths, parent_selectors)
        self.multiple = multiple
        self.delay = delay
        self.regex = regex

    @classmethod
    def get_features(cls):
        base_features = Selector.get_features()
        base_features.update(cls.features)
        return base_features

    def will_return_multiple_records(self):
        return self.can_return_multiple_records and self.multiple

    def will_return_elements(self):
        return self.can_return_elements

    def will_return_new_jobs(self):
        return self.can_create_new_jobs

    def will_return_local_childs(self):
        return self.can_have_local_child_selectors

    def get_specific_data(self, parentElement):
        elements = self.get_data_elements(parentElement)

        resultData = list()

        for element in elements:
            data = dict()
            text = pq(element).text()
            data[self.id] = text
            resultData.append(data)

        if not self.multiple and len(elements) == 0:
            data = dict()
            data[self.id] = None
            resultData.append(data)

        return resultData