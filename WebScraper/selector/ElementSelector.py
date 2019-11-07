#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/4/17 9:09 AM
# @Author  : mirko
# @FileName: ElementSelector.py
# @Software: PyCharm

from . import RegisterSelectorType, Selector


@RegisterSelectorType("SelectorElement")
class ElementSelector(Selector):

    can_return_multiple_records = True
    can_have_child_selectors = True
    can_have_local_child_selectors = True
    can_create_new_jobs = False
    can_return_elements = True

    features = {
        "multiple": False,
        "delay": 0
    }

    def __init__(self, id, type, css_paths, parent_selectors, multiple, delay, **kwargs):
        super(ElementSelector, self).__init__(id, type, css_paths, parent_selectors)
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

    def get_specific_data(self, driver, job_url, parentElement):
        elements = self.get_data_elements(driver ,job_url, parentElement)

        return list(elements)

