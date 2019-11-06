#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/4/22 9:20 PM
# @Author  : mirko
# @FileName: LinkSelector.py
# @Software: PyCharm

from . import RegisterSelectorType, Selector
from pyquery import PyQuery as pq

@RegisterSelectorType("SelectorLink")
class LinkSelector(Selector):

    can_return_multiple_records = True
    can_have_child_selectors = True
    can_have_local_child_selectors = False
    can_create_new_jobs = True
    can_return_elements = False

    features = {
        'multiple': False,
        'delay': 0
    }

    def __init__(self, id, type, css_paths, parent_selectors, multiple, delay, **kwargs):
        super(LinkSelector, self).__init__(id, type, css_paths, parent_selectors)
        self.multiple = multiple
        self.delay = delay

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
        resultData = list()
        elements = self.get_data_elements(parentElement)

        if not self.multiple and len(elements) == 0:
            data = dict()
            data[self.id] = None
            resultData.append(data)
            return resultData


        for element in elements:
            pq_object = pq(element)
            data = dict()
            data[self.id] = pq_object.text()
            data["_followSelectorId"] = self.id
            data[str(self.id) + "-href"] = pq_object.attr("href")
            data["_follow"] = pq_object.attr("href")

            resultData.append(data)

        return resultData